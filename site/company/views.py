
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, ListView

import stripe

from braces.views import CsrfExemptMixin
from djstripe.models import Customer, CurrentSubscription
from djstripe.settings import (PAYMENT_PLANS, subscriber_request_callback,
                               CANCELLATION_AT_PERIOD_END)
from djstripe.sync import sync_subscriber
from djstripe.views import (
    AccountView as DjStripeAccountView,
    ChangeCardView as DjStripeChangeCardView,
    HistoryView as DjStripeHistoryView,
    # SyncHistoryView as DjStripeSyncHistoryView,
    ConfirmFormView as DjStripeConfirmFormView,
    SubscribeView as DjStripeSubscribeView,
    ChangePlanView as DjStripeChangePlanView,
    CancelSubscriptionView as DjStripeCancelSubscriptionView
)

from shareholder.models import Company
from utils.mail import is_valid_email
from utils.subscriptions import (stripe_company_shareholder_invoice_item,
                                 stripe_company_security_invoice_item)

from .mixins import (CompanyOperatorPermissionRequiredViewMixin,
                     SubscriptionViewCompanyObjectMixin)


@login_required
def company(request, company_id):
    template = loader.get_template('company.html')
    company = get_object_or_404(Company, id=int(company_id))
    context = RequestContext(request, {'company': company})
    return HttpResponse(template.render(context))


# djstripe views

class SubscriptionsListView(ListView):

    template_name = 'subscriptions.html'
    allow_empty = False

    def get_queryset(self):
        company_ids = self.request.user.operator_set.all().values_list(
            'company_id')
        return Company.objects.filter(pk__in=company_ids)


subscriptions = login_required(SubscriptionsListView.as_view())


class AccountView(CompanyOperatorPermissionRequiredViewMixin,
                  SubscriptionViewCompanyObjectMixin, DjStripeAccountView):

    def get_context_data(self, *args, **kwargs):
        context = super(AccountView, self).get_context_data(*args, **kwargs)
        customer, plans = context.get('customer'), context.get('plans', [])
        for plan in plans:
            is_subscribable = customer.subscriber.can_subscribe_plan(
                plan.get('plan'))
            if not is_subscribable:
                plan.update(dict(unsubscribable=True))
        return context


class ChangeCardView(CompanyOperatorPermissionRequiredViewMixin,
                     SubscriptionViewCompanyObjectMixin,
                     DjStripeChangeCardView):

    def get_post_success_url(self):
        return reverse('djstripe:account',
                       kwargs=dict(company_id=self.kwargs.get('company_id')))


class ConfirmFormView(CompanyOperatorPermissionRequiredViewMixin,
                      SubscriptionViewCompanyObjectMixin,
                      DjStripeConfirmFormView):

    success_url = None

    def get(self, request, *args, **kwargs):
        plan_slug = self.kwargs['plan']
        if plan_slug not in PAYMENT_PLANS:
            return redirect("djstripe:subscribe",
                            company_id=kwargs.get('company_id'))

        plan = PAYMENT_PLANS[plan_slug]
        customer, created = Customer.get_or_create(
            subscriber=subscriber_request_callback(self.request))

        if (hasattr(customer, "current_subscription") and
                customer.current_subscription.plan == plan['plan'] and
                (customer.current_subscription.status !=
                 CurrentSubscription.STATUS_CANCELLED)):
            message = _("You already subscribed to this plan")
            messages.info(request, message, fail_silently=True)
            return redirect("djstripe:subscribe",
                            company_id=kwargs.get('company_id'))

        return super(ConfirmFormView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(ConfirmFormView, self).get_context_data(
            *args, **kwargs)
        customer, plan = context.get('customer'), context.get('plan')
        # check if plan is subscribable
        is_subscribable, errors = customer.subscriber.validate_plan(
            plan.get('plan'))
        if not is_subscribable:
            context['plan_unsubscribable'] = True
            context['plan_errors'] = errors
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            post_data = self.request.POST
            try:
                customer, created = Customer.get_or_create(
                    subscriber=subscriber_request_callback(self.request))
                customer.update_card(post_data.get("stripe_token"))

                # update customer email (if necessary)
                email = post_data.get('email')
                if is_valid_email(email) and not customer.subscriber.email:
                    customer.subscriber.email = email
                    customer.subscriber.save()

                plan = form.cleaned_data['plan']

                # check if plan is subscribable
                is_subscribable, errors = customer.subscriber.validate_plan(
                    plan)
                if not is_subscribable:
                    for error in errors:
                        form.add_error(None, error.messages[0])
                    return self.form_invalid(form)

                # create invoiceitem for shareholders if necessary
                stripe_company_shareholder_invoice_item(customer, plan)

                # create invoiceitem for securities if necessary
                stripe_company_security_invoice_item(customer, plan)

                # subscribe customer to selected plan
                customer.subscribe(plan)
            except stripe.StripeError as exc:
                form.add_error(None, str(exc))
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('djstripe:history',
                       kwargs=dict(company_id=self.kwargs.get('company_id')))


class ChangePlanView(CompanyOperatorPermissionRequiredViewMixin,
                     SubscriptionViewCompanyObjectMixin,
                     DjStripeChangePlanView):

    success_url = None

    def get_success_url(self):
        return reverse('djstripe:history',
                       kwargs=dict(company_id=self.kwargs.get('company_id')))


class CancelSubscriptionView(CompanyOperatorPermissionRequiredViewMixin,
                             SubscriptionViewCompanyObjectMixin,
                             DjStripeCancelSubscriptionView):

    success_url = None

    def get_success_url(self):
        return reverse('djstripe:account',
                       kwargs=dict(company_id=self.kwargs.get('company_id')))

    def form_valid(self, form):
        customer, created = Customer.get_or_create(
            subscriber=subscriber_request_callback(self.request))
        current_subscription = customer.cancel_subscription(
            at_period_end=CANCELLATION_AT_PERIOD_END)

        if (current_subscription.status ==
                current_subscription.STATUS_CANCELLED):
            # If no pro-rate, they get kicked right out.
            messages.info(self.request, "Your subscription is now cancelled.")
            # logout the user
            auth_logout(self.request)
            return redirect("start")
        else:
            # If pro-rate, they get some time to stay.
            messages.info(
                self.request,
                _("Your subscription status is now '{status}' until "
                  "'{period_end}'").format(
                    status=current_subscription.status,
                    period_end=current_subscription.current_period_end)
            )

        return super(CancelSubscriptionView, self).form_valid(form)


class HistoryView(CompanyOperatorPermissionRequiredViewMixin,
                  SubscriptionViewCompanyObjectMixin, DjStripeHistoryView):
    pass


class SyncHistoryView(CsrfExemptMixin,
                      CompanyOperatorPermissionRequiredViewMixin,
                      SubscriptionViewCompanyObjectMixin, View):

    template_name = "djstripe/includes/_history_table.html"

    def post(self, request, *args, **kwargs):
        context = dict(
            customer=sync_subscriber(subscriber_request_callback(request))
        )
        return render(request, self.template_name, context)


class SubscribeView(CompanyOperatorPermissionRequiredViewMixin,
                    SubscriptionViewCompanyObjectMixin, DjStripeSubscribeView):

    def get_context_data(self, *args, **kwargs):
        context = super(SubscribeView, self).get_context_data(*args, **kwargs)
        customer = context.get('customer')
        plans = context.get('PAYMENT_PLANS', [])
        for plan in plans:
            is_subscribable, errors = customer.subscriber.validate_plan(plan)
            if not is_subscribable:
                plans[plan].update(dict(unsubscribable=True, errors=errors))
        return context


# subscription views
account = AccountView.as_view()
change_card = ChangeCardView.as_view()
history = HistoryView.as_view()
sync_history = SyncHistoryView.as_view()
confirm = ConfirmFormView.as_view()
subscribe = SubscribeView.as_view()
change_plan = ChangePlanView.as_view()
# cancel_subscription = CancelSubscriptionView.as_view()
