
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import RequestContext, loader
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

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
from utils.payment import stripe_company_shareholder_invoice_item

from .mixins import (CompanyOperatorPermissionRequiredViewMixin,
                     PaymentViewCompanyObjectMixin)


@login_required
def company(request, company_id):
    template = loader.get_template('company.html')
    company = get_object_or_404(Company, id=int(company_id))
    context = RequestContext(request, {'company': company})
    return HttpResponse(template.render(context))


# djstripe views

class AccountView(CompanyOperatorPermissionRequiredViewMixin,
                  PaymentViewCompanyObjectMixin, DjStripeAccountView):
    pass


class ChangeCardView(CompanyOperatorPermissionRequiredViewMixin,
                     PaymentViewCompanyObjectMixin, DjStripeChangeCardView):

    def get_post_success_url(self):
        return reverse('djstripe:account',
                       kwargs=dict(company_id=self.kwargs.get('company_id')))


class ConfirmFormView(CompanyOperatorPermissionRequiredViewMixin,
                      PaymentViewCompanyObjectMixin, DjStripeConfirmFormView):

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

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            try:
                customer, created = Customer.get_or_create(
                    subscriber=subscriber_request_callback(self.request))
                customer.update_card(self.request.POST.get("stripe_token"))

                plan = form.cleaned_data['plan']
                # create invoiceitem for shareholders if necessary
                stripe_company_shareholder_invoice_item(customer, plan)
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
                     PaymentViewCompanyObjectMixin, DjStripeChangePlanView):

    success_url = None

    def get_success_url(self):
        return reverse('djstripe:history',
                       kwargs=dict(company_id=self.kwargs.get('company_id')))


class CancelSubscriptionView(CompanyOperatorPermissionRequiredViewMixin,
                             PaymentViewCompanyObjectMixin,
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
                  PaymentViewCompanyObjectMixin, DjStripeHistoryView):
    pass


class SyncHistoryView(CsrfExemptMixin,
                      CompanyOperatorPermissionRequiredViewMixin,
                      PaymentViewCompanyObjectMixin, View):

    template_name = "djstripe/includes/_history_table.html"

    def post(self, request, *args, **kwargs):
        context = dict(
            customer=sync_subscriber(subscriber_request_callback(request))
        )
        return render(request, self.template_name, context)


class SubscribeView(CompanyOperatorPermissionRequiredViewMixin,
                    PaymentViewCompanyObjectMixin, DjStripeSubscribeView):
    pass


# payment views
account = AccountView.as_view()
change_card = ChangeCardView.as_view()
history = HistoryView.as_view()
sync_history = SyncHistoryView.as_view()
confirm = ConfirmFormView.as_view()
subscribe = SubscribeView.as_view()
change_plan = ChangePlanView.as_view()
cancel_subscription = CancelSubscriptionView.as_view()
