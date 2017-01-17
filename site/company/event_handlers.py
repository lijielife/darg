
from djstripe import webhooks

from utils.mail import is_valid_email


@webhooks.handler(['invoice.created'])
def invoice_webhook_handler(event, event_data, event_type, event_subtype):
    # from djstripe.models import Customer
    from utils.subscriptions import (stripe_company_shareholder_invoice_item,
                                     stripe_company_security_invoice_item)

    customer = event.customer
    invoice_object = event.message.get('data', {}).get('object', {})
    if (not invoice_object.get('closed') and
            event.customer.has_active_subscription()):
        # add per shareholder fee to invoice
        stripe_company_shareholder_invoice_item(
            customer,
            customer.current_subscription.plan,
            invoice=invoice_object.get('id')
        )
        # add per security fee to invoice
        stripe_company_security_invoice_item(
            customer,
            customer.current_subscription.plan,
            invoice=invoice_object.get('id')
        )


@webhooks.handler(['customer'])
def customer_webhook_handler(event, event_data, event_type, event_subtype):
    """
    use customer email address for subscriber if no email set on subscriber
    instance, also set address (if necessary/possible)
    """
    subscriber = event.customer.subscriber
    object_data = event.validated_message.get('data', {}).get('object', {})

    # email
    if not subscriber.email:
        email = object_data.get('email') or object_data.get('name')

        if is_valid_email(email):
            subscriber.email = email
            subscriber.save()

    if not subscriber.has_address:
        subscriber.read_address_from_stripe_object(object_data)
