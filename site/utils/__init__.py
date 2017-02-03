
from django.conf import settings


def get_vat(amount, net_value=False):
    """
    return VAT value for `amount` (settings.COMPANY_INVOICE_VAT)

    use net_value to get the net amount (default: False)
    """
    vat = settings.COMPANY_INVOICE_VAT
    amount = amount or 0
    net = amount / (100 + vat) * 100
    return net_value and net or amount - net
