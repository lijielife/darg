
from django.dispatch import receiver

from djstripe.signals import WEBHOOK_SIGNALS

from .signals import stripe_invoice_created_handler


receiver(WEBHOOK_SIGNALS['invoice.created'])(stripe_invoice_created_handler)
