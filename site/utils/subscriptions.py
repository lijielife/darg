
from django.utils.translation import ugettext_lazy as _

import stripe


def stripe_subscriber_request_callback(request):
    """
    get Company (subscription model) via request
    """
    from django.apps import apps
    from django.conf import settings

    subscriber_model = apps.get_model(settings.DJSTRIPE_SUBSCRIBER_MODEL)
    kwargs = request.resolver_match.kwargs
    pk = kwargs.get('{}_id'.format(subscriber_model._meta.model_name))
    return subscriber_model.objects.filter(pk=pk).first()


def stripe_company_shareholder_invoice_item(customer, plan, invoice=None):
    """
    create an invoice item for all active company shareholders (if in settings)
    """
    from django.conf import settings

    def _get_company_shareholder_count(company, date=None):
        """
        return count of active shareholders but exclude company shareholder
        """
        count = 0
        shareholders = company.shareholder_set.exclude(number='0')
        for shareholder in shareholders.order_by('number'):
            if shareholder.share_count(date=date) > 0:
                count += 1
        return count

    plan_config = settings.PLAN_FEATURE_CONFIG.get(plan, {})
    price_per_shareholder = plan_config.get('shareholder_price')
    if price_per_shareholder:
        # add per shareholder fees as InvoiceItems for customer
        shareholder_count = _get_company_shareholder_count(customer.subscriber)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.InvoiceItem.create(
            customer=customer.stripe_id,
            amount=price_per_shareholder * shareholder_count,
            currency=settings.DJSTRIPE_CURRENCIES[0][0],
            invoice=invoice,
            description=_(
                'Shareholders ({count} x {amount:.2f})').format(
                **dict(count=shareholder_count,
                       amount=price_per_shareholder / float(100)))
        )


def stripe_company_security_invoice_item(customer, plan, invoice=None):
    """
    create an invoice item for extra company securities (if in settings)
    """
    from django.conf import settings

    plan_config = settings.PLAN_FEATURE_CONFIG.get(plan)
    price_per_security = plan_config.get('security_price')
    security_count = customer.subscriber.security_set.count()
    billable_securities = security_count - 1  # one is always free
    if price_per_security and max(0, billable_securities):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.InvoiceItem.create(
            customer=customer.stripe_id,
            amount=price_per_security * billable_securities,
            currency=settings.DJSTRIPE_CURRENCIES[0][0],
            invoice=invoice,
            description=_(
                'Extra Securities ({count} x {amount:.2f})').format(
                **dict(count=billable_securities,
                       amount=price_per_security / float(100)))
        )
