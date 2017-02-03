
from django.conf import settings
from django.test import TestCase

from djstripe.models import CurrentSubscription, Customer, Event, Invoice
from mock import MagicMock, patch
from model_mommy import mommy, random_gen

from ..event_handlers import (invoice_created_webhook_handler,
                              invoice_payment_succeeded_webhook_handler,
                              customer_webhook_handler)


class StripeWebhookHandlerTestCase(TestCase):

    def setUp(self):
        super(StripeWebhookHandlerTestCase, self).setUp()

        self.subscriber = mommy.make(settings.DJSTRIPE_SUBSCRIBER_MODEL)
        self.customer = mommy.make(Customer, subscriber=self.subscriber)

    @patch('utils.subscriptions.stripe_company_shareholder_invoice_item')
    @patch('utils.subscriptions.stripe_company_security_invoice_item')
    def test_invoice_created_webhook_handler(self, mock_security_invoice_item,
                                             mock_shareholder_invoice_item):

        global add_shareholder_item
        global add_security_item
        add_shareholder_item, add_security_item = 0, 0

        def shareholder_side_effect(*args, **kwargs):
            globals()['add_shareholder_item'] += 1

        mock_shareholder_invoice_item.side_effect = shareholder_side_effect

        def security_side_effect(*args, **kwargs):
            globals()['add_security_item'] += 1

        mock_security_invoice_item.side_effect = security_side_effect

        handler = invoice_created_webhook_handler
        event = mommy.make(Event,
                           stripe_id='evt_{}'.format(
                               random_gen.gen_uuid().hex[-24:]),
                           customer=None,
                           webhook_message=dict(),
                           validated_message=dict())

        # no customer
        self.assertIsNone(handler(None, event))

        event.customer = self.customer
        event.save()

        # 'closed' not in invoice data
        handler(None, event)
        self.assertEqual(add_shareholder_item, 0)
        self.assertEqual(add_security_item, 0)

        event.validated_message['data'] = {'object': {
            'id': 'in_{}'.format(random_gen.gen_uuid().hex[-24:]),
            'closed': True
        }}
        event.save()

        # 'closed' is True in invoice data
        handler(None, event)
        self.assertEqual(add_shareholder_item, 0)
        self.assertEqual(add_security_item, 0)

        event.validated_message['data']['object']['closed'] = False
        event.save()

        # 'closed' is False but customer has no active subscription
        handler(None, event)
        self.assertEqual(add_shareholder_item, 0)
        self.assertEqual(add_security_item, 0)

        # add (fake) subscription
        event.customer.current_subscription = mommy.make(CurrentSubscription)

        with patch.object(self.customer, 'has_active_subscription',
                          return_value=True):

            handler(None, event)
            self.assertEqual(add_shareholder_item, 1)
            self.assertEqual(add_security_item, 1)

    def tests_invoice_payment_succeeded_webhook_handler(self):
        handler = invoice_payment_succeeded_webhook_handler
        event = mommy.make(Event,
                           stripe_id='evt_{}'.format(
                               random_gen.gen_uuid().hex[-24:]),
                           customer=None,
                           webhook_message=dict(),
                           validated_message=dict())

        # no customer
        self.assertIsNone(handler(None, event))

        event.customer = self.customer
        event.save()

        stripe_id = 'in_{}'.format(random_gen.gen_uuid().hex[-24:])
        mommy.make(Invoice, stripe_id=stripe_id, customer=event.customer)

        event.validated_message['data'] = {'object': {'id': stripe_id}}

        with patch.object(Invoice, '_generate_invoice_pdf') as mock_pdf_gen:

            global pdf_generated
            pdf_generated = 0

            def side_effect(*args, **kwargs):
                globals()['pdf_generated'] += 1

            mock_pdf_gen.side_effect = side_effect

            handler(None, event)

            self.assertEqual(pdf_generated, 1)

    def test_customer_webhook_handler(self):
        handler = customer_webhook_handler
        event = mommy.make(Event,
                           stripe_id='evt_{}'.format(
                               random_gen.gen_uuid().hex[-24:]),
                           customer=None,
                           webhook_message=dict(),
                           validated_message=dict())
        event_data, event_type, event_subtype = dict(), 'customer', 'updated'

        # no customer
        self.assertIsNone(
            handler(event, event_data, event_type, event_subtype)
        )

        event.customer = self.customer
        email1 = random_gen.gen_email()
        event.validated_message['data'] = {'object': {'email': email1}}
        event.save()

        handler(event, event_data, event_type, event_subtype)

        self.assertEqual(event.customer.subscriber.email, email1)

        # test name fallback
        email2 = random_gen.gen_email()
        event.validated_message['data'] = {'object': {'name': email2}}
        event.save()

        handler(event, event_data, event_type, event_subtype)

        # email not changed because alread set
        self.assertEqual(event.customer.subscriber.email, email1)

        event.customer.subscriber.email = ''
        handler(event, event_data, event_type, event_subtype)
        self.assertEqual(event.customer.subscriber.email, email2)

        # test invalid email
        event.customer.subscriber.email = ''
        event.validated_message['data'] = {'object': {'email': 'foobar'}}
        handler(event, event_data, event_type, event_subtype)
        self.assertEqual(event.customer.subscriber.email, '')

        # test read address call
        mock_read_address = MagicMock()

        global address_read
        address_read = 0

        def side_effect(*args, **kwargs):
            globals()['address_read'] += 1

        mock_read_address.side_effect = side_effect
        event.customer.subscriber.read_address_from_stripe_object = (
            mock_read_address)

        handler(event, event_data, event_type, event_subtype)

        self.assertEqual(address_read, 1)
