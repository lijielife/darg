
from djstripe import webhooks

from utils.mail import is_valid_email


@webhooks.handler(['invoice.created'])
def invoice_created_webhook_handler(event, event_data, event_type,
                                    event_subtype):
    """
    handler for invoice.created event

    add any pending invoice items if invoice not closed yet
    """

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


@webhooks.handler(['invoice.payment_succeeded'])
def invoice_payment_succeeded_webhook_handler(event, event_data, event_type,
                                              event_subtype):
    """
    handler for invoice.payment_succeeded event

    trigger invoice pdf (re)generation
    """
    customer = event.customer
    invoice_object = event.message.get('data', {}).get('object', {})
    invoice = customer.invoices.filter(
        stripe_id=invoice_object.get('id')).first()
    invoice and invoice._generate_invoice_pdf(override_existing=True)


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
