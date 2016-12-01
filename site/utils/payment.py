
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
    create an invoice item for all active company shareholders
    (if plan has settings.PAYMENT_PER_SHAREHOLDER)
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

    price_per_shareholder = settings.PAYMENT_PER_SHAREHOLDER.get(
        plan)
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
                'Shareholders ({count} x {amount})').format(
                **dict(count=shareholder_count,
                       amount=price_per_shareholder / float(100)))
        )
