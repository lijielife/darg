import collections
import decimal

import stripe
from braces.views import CsrfExemptMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, View
# from company.forms import PlanForm  # stripe 1.0+
from djstripe.forms import PlanForm
from djstripe.models import CurrentSubscription, Customer, Invoice
from djstripe.settings import (PAYMENT_PLANS,  # CANCELLATION_AT_PERIOD_END,
                               PLAN_LIST, PRORATION_POLICY_FOR_UPGRADES,
                               subscriber_request_callback)
from djstripe import settings
from djstripe.sync import sync_subscriber
from djstripe.views import AccountView as DjStripeAccountView  # SyncHistoryView as DjStripeSyncHistoryView,; CancelSubscriptionView as DjStripeCancelSubscriptionView
from djstripe.views import ChangeCardView as DjStripeChangeCardView
from djstripe.views import ChangePlanView as DjStripeChangePlanView
from djstripe.views import ConfirmFormView as DjStripeConfirmFormView
from djstripe.views import HistoryView as DjStripeHistoryView
from djstripe.views import SubscribeView as DjStripeSubscribeView
from sendfile import sendfile

import utils
from shareholder.models import Company, Operator

from .mixins import (CompanyOperatorPermissionRequiredViewMixin,
                     SubscriptionViewCompanyObjectMixin)


# from utils.mail import is_valid_email
# from utils.subscriptions import (stripe_company_shareholder_invoice_item,
#                                  stripe_company_security_invoice_item)


@login_required
def company(request, company_id):
    """
    show company detail page
    """
    template = loader.get_template('company.html')
    company = get_object_or_404(Company.objects.filter(
        operator__user=request.user), id=int(company_id))
    context = {'company': company}
    return HttpResponse(template.render(context=context, request=request))


# djstripe views

class SubscriptionsListView(ListView):

    template_name = 'subscriptions.html'
    allow_empty = False

    def get_queryset(self):
        company_ids = self.request.user.operator_set.all().values_list(
            'company_id')
        return Company.objects.filter(pk__in=company_ids)

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if self.object_list.count() == 1:
            # redirect to company subscription account page
            return redirect(
                'djstripe:account', company_id=self.object_list.first().pk)

        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None and
                    hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(
                    _("Empty list and '%(class_name)s.allow_empty' is False.")
                    % {'class_name': self.__class__.__name__})
        context = self.get_context_data()
        return self.render_to_response(context)


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
        plan_slug = self.kwargs.get('plan')
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
        customer, plan = context.get('customer'), context.get('plan', {})
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
                if (utils.mail.is_valid_email(email) and
                        not customer.subscriber.email):
                    customer.subscriber.email = email
                    customer.subscriber.save()

                plan = form.cleaned_data['plan']

                # check if plan is subscribable
                is_subscribable, errors = customer.subscriber.validate_plan(
                    plan)
                if not is_subscribable:
                    # for error in errors:
                    #     form.add_error(None, error.messages[0])
                    [form.add_error(None, err.messages[0]) for err in errors]
                    return self.form_invalid(form)

                # create invoiceitem for shareholders if necessary
                utils.subscriptions.stripe_company_shareholder_invoice_item(
                    customer, plan)

                # create invoiceitem for securities if necessary
                utils.subscriptions.stripe_company_security_invoice_item(
                    customer, plan)

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

    def post(self, request, *args, **kwargs):
        form = PlanForm(request.POST)
        try:
            customer = subscriber_request_callback(request).customer
        except Customer.DoesNotExist as exc:
            error_message = _("You must already be subscribed to a plan before"
                              " you can change it.")
            form.add_error(None, error_message)
            return self.form_invalid(form)

        if form.is_valid():
            plan_name = form.cleaned_data["plan"]

            # check if plan is subscribable
            is_subscribable, errors = customer.subscriber.validate_plan(
                plan_name)
            if not is_subscribable:
                # for error in errors:
                #     form.add_error(None, error.messages[0])
                [form.add_error(None, err.messages[0]) for err in errors]
                return self.form_invalid(form)

            try:
                # When a customer upgrades their plan, and
                # DJSTRIPE_PRORATION_POLICY_FOR_UPGRADES is set to True,
                # we force the proration of the current plan and use it towards
                # the upgraded plan, no matter what DJSTRIPE_PRORATION_POLICY
                # is set to.
                prorate = False
                if PRORATION_POLICY_FOR_UPGRADES:
                    current_subscription_amount = (
                        customer.current_subscription.amount)
                    selected_plan = next(plan for plan in PLAN_LIST
                                         if plan.get('plan') == plan_name)
                    selected_plan_price = (
                        selected_plan["price"] / decimal.Decimal(100))

                    # Is it an upgrade?
                    if selected_plan_price > current_subscription_amount:
                        prorate = True

                # create invoiceitem for shareholders if necessary
                utils.subscriptions.stripe_company_shareholder_invoice_item(
                    customer, plan_name)

                # create invoiceitem for securities if necessary
                utils.subscriptions.stripe_company_security_invoice_item(
                    customer, plan_name)

                customer.subscribe(plan_name, prorate=prorate)
            except stripe.StripeError as exc:
                form.add_error(None, str(exc))
                return self.form_invalid(form)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('djstripe:history',
                       kwargs=dict(company_id=self.kwargs.get('company_id')))

# class CancelSubscriptionView(CompanyOperatorPermissionRequiredViewMixin,
#                              SubscriptionViewCompanyObjectMixin,
#                              DjStripeCancelSubscriptionView):
#
#     success_url = None
#
#     def get_success_url(self):
#         return reverse('djstripe:account',
#                        kwargs=dict(company_id=self.kwargs.get('company_id')))
#
#     def form_valid(self, form):
#         customer, created = Customer.get_or_create(
#             subscriber=subscriber_request_callback(self.request))
#         current_subscription = customer.cancel_subscription(
#             at_period_end=CANCELLATION_AT_PERIOD_END)
#
#         if (current_subscription.status ==
#                 current_subscription.STATUS_CANCELLED):
#             # If no pro-rate, they get kicked right out.
#             messages.info(self.request,
#                           _("Your subscription is now cancelled."))
#             # logout the user
#             # auth_logout(self.request)
#             return redirect("start")
#         else:
#             # If pro-rate, they get some time to stay.
#             messages.info(
#                 self.request,
#                 _("Your subscription status is now '{status}' until "
#                   "'{period_end}'").format(
#                     status=current_subscription.status,
#                     period_end=current_subscription.current_period_end)
#             )
#
#         return super(CancelSubscriptionView, self).form_valid(form)


class HistoryView(CompanyOperatorPermissionRequiredViewMixin,
                  SubscriptionViewCompanyObjectMixin, DjStripeHistoryView):
    pass


class SyncHistoryView(CsrfExemptMixin,
                      CompanyOperatorPermissionRequiredViewMixin,
                      SubscriptionViewCompanyObjectMixin, View):

    template_name = "djstripe/includes/_history_table.html"

    def post(self, request, *args, **kwargs):
        context = dict(
            customer=sync_subscriber(settings.subscriber_request_callback(request))
        )
        return render(request, self.template_name, context)


class SubscribeView(CompanyOperatorPermissionRequiredViewMixin,
                    SubscriptionViewCompanyObjectMixin, DjStripeSubscribeView):

    def get_context_data(self, *args, **kwargs):
        context = super(SubscribeView, self).get_context_data(*args, **kwargs)
        customer = context.get('customer')
        plans = context.get('PAYMENT_PLANS', collections.OrderedDict())
        for plan in plans:
            is_subscribable, errors = customer.subscriber.validate_plan(plan)
            if not is_subscribable:
                plans[plan].update(dict(unsubscribable=True, errors=errors))
        return context


class InvoiceDetailView(CompanyOperatorPermissionRequiredViewMixin,
                        SubscriptionViewCompanyObjectMixin, DetailView):
    """
    return PDF of invoice/charge
    """

    def get_queryset(self):
        company_pk = self.kwargs.get('company_id', 0)
        return Invoice.objects.filter(customer__subscriber_id=company_pk)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_invoice_pdf:
            # try to generate now
            self.object._generate_invoice_pdf()

        if not self.object.has_invoice_pdf:
            # FIXME: what now (logger exception, mail_managery)?
            error_message = _('Could not find requested filed.')
            raise Http404(error_message)

        return sendfile(request, self.object._get_pdf_filepath())


# subscription views
account = AccountView.as_view()
change_card = ChangeCardView.as_view()
history = HistoryView.as_view()
sync_history = SyncHistoryView.as_view()
confirm = ConfirmFormView.as_view()
subscribe = SubscribeView.as_view()
change_plan = ChangePlanView.as_view()
# cancel_subscription = CancelSubscriptionView.as_view()
invoice = InvoiceDetailView.as_view()


@login_required
def company_select(request):
    """
    view to select company to work within for operators
    """
    template = loader.get_template('company_select.html')

    # company choice: set to session and redirect to start...
    company_id = int(request.GET.get('company_id', 0))
    if company_id:
        operator = get_object_or_404(Operator, company__pk=company_id,
                                     user=request.user)
        request.session['company_pk'] = operator.company.pk
        return redirect("start")

    # add new corp, clean session and redirect to start...
    if request.GET.get('add_company'):
        if request.session.get('company_pk'):
            del request.session['company_pk']
        return redirect("start")

    # render company choice view
    return HttpResponse(template.render(request=request))
