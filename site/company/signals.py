
def stripe_invoice_created_handler(sender, **kwargs):
    from djstripe.models import Customer
    from utils.payment import stripe_company_shareholder_invoice_item

    event = kwargs.get('event')
    customer = Customer.objects.first()  # event.customer
    invoice_object = event.message.get('data', {}).get('object', {})
    if (not invoice_object.get('closed') and
            event.customer.has_active_subscription()):
        # add per shareholder fee to invoice
        stripe_company_shareholder_invoice_item(
            customer,
            customer.current_subscription.plan,
            invoice=invoice_object.get('id')
        )
