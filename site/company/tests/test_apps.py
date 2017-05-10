
import os
import shutil
import tempfile

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.test import TestCase, override_settings

from djstripe.models import Charge, Invoice, InvoiceItem
from mock import patch
from model_mommy import mommy, random_gen

from project.tests.helper import TestLoggingHandler, FakeStripeResponser
from project.tests.mixins import StripeTestCaseMixin
from shareholder.tests.mixins import AddressTestMixin
# from shareholder.models import Company

from ..apps import logger


class ChargeTweakTestCase(StripeTestCaseMixin, AddressTestMixin, TestCase):

    @classmethod
    def setUpClass(cls):
        super(ChargeTweakTestCase, cls).setUpClass()

        cls._test_logging_handler = TestLoggingHandler(level='DEBUG')
        # logger.addHandler(cls._test_logging_handler)
        logger.handlers = [cls._test_logging_handler]
        cls._log_messages = cls._test_logging_handler.messages

    def setUp(self):
        super(ChargeTweakTestCase, self).setUp()

        # reset test log handler for each test
        self._test_logging_handler.reset()

        self.charge = mommy.make(Charge)
        self.fake_responser = FakeStripeResponser('get', '/v1/customers/')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.dummy')
    @patch.object(EmailMultiAlternatives, 'send')
    @patch.object(EmailMultiAlternatives, 'attach')
    def test_send_receipt(self, mock_attach, mock_send):

        self.assertFalse(self.charge.receipt_sent)
        self.assertIsNone(self.charge.amount)

        # don't send receipt if no amount
        self.charge.send_receipt()
        self.assertFalse(self.charge.receipt_sent)
        mock_send.assert_not_called()

        # don't send receipt if already sent
        self.charge.amount = abs(random_gen.gen_float())
        self.charge.save()
        self.charge.receipt_sent = True
        self.charge.save()
        self.assertTrue(self.charge.receipt_sent)
        self.assertIsNotNone(self.charge.amount)
        self.charge.send_receipt()
        mock_send.assert_not_called()

        self.charge.receipt_sent = False
        self.charge.save()

        # create subscriber (with no email)
        subscriber = mommy.make(settings.DJSTRIPE_SUBSCRIBER_MODEL)
        self.charge.customer.subscriber = subscriber
        self.charge.customer.save()
        self.assertFalse(bool(subscriber.email))

        with patch.object(self.charge, '_get_customer_data') as mock_data:
            mock_data.return_value = self.fake_responser.get_response()

            self.charge.send_receipt()
            mock_send.assert_called()
            self.assertTrue(bool(self.charge.customer.subscriber.email))
            # check postal error
            self.assertEqual(len(self._log_messages.get('error')), 1)
            self._test_logging_handler.reset()

            # reset email for next test
            self.charge.customer.subscriber.email = ''
            self.charge.customer.subscriber.save()
            self.charge.receipt_sent = False

            mock_send.reset_mock()

            with patch('utils.mail.is_valid_email', return_value=False):
                self.charge.send_receipt()
                # check log error
                self.assertEqual(len(self._log_messages.get('error')), 1)
                self._test_logging_handler.reset()
                # no email sent
                mock_send.assert_not_called()

        # add company address and email
        self.add_address(subscriber)

        subscriber.email = random_gen.gen_email()
        subscriber.save()
        self.assertTrue(self.charge.customer.subscriber.has_address)
        self.assertTrue(bool(self.charge.customer.subscriber.email))

        self.charge.send_receipt()
        mock_send.assert_called()

        mock_send.reset_mock()

        # reset sent
        self.charge.receipt_sent = False

        # add invoice
        self.charge.invoice = mommy.make(Invoice)
        self.charge.save()

        # check attachments
        mock_attach.assert_not_called()

        example_invoice = os.path.join(
            os.path.dirname(__file__), 'files', 'example.pdf')
        with patch.object(self.charge.invoice, '_generate_invoice_pdf',
                          return_value=example_invoice):
            self.charge.send_receipt()
            mock_send.assert_called()
            mock_attach.assert_called()

        mock_send.reset_mock()

        # check receipt_sent when email fails
        self.charge.receipt_sent = False
        self.charge.invoice = None
        self.charge.save()

        self.charge.send_receipt()
        # self.assertFalse(self.charge.receipt_sent)  # FIXME
        mock_send.assert_called()

    @patch('stripe.Customer.retrieve')
    def test_get_customer_data(self, mock_retrieve):

        mock_retrieve.side_effect = Exception()

        data = self.charge._get_customer_data()
        self.assertNotIn('id', data)
        self.assertEqual(data, dict())

        mock_retrieve.side_effect = None
        mock_retrieve.return_value = self.fake_responser.get_response()
        data = self.charge._get_customer_data()
        self.assertIn('id', data)

    def test_get_template_context(self):

        # check simple stuff first
        context = self.charge._get_template_context()
        self.assertEqual(context.get('charge'), self.charge)
        self.assertIn('site', context)
        self.assertIn('STATIC_URL', context)
        self.assertIn('invoice_items', context)
        self.assertEqual(len(context.get('invoice_items')), 0)
        self.assertIn('company', context)
        self.assertIn('protocol', context)
        self.assertIn('include_vat', context)

        # no items, check fallback currency
        with self.settings(DJSTRIPE_CURRENCIES=(('usd', 'US Dollar'),)):
            context = self.charge._get_template_context()
            self.assertEqual(context.get('currency'), 'usd')

        # check vat setting
        with self.settings(COMPANY_INVOICE_INCLUDE_VAT=False):
            context = self.charge._get_template_context()
            self.assertFalse(context.get('include_vat'))
            self.assertNotIn('vat', context)
            self.assertNotIn('vat_value', context)

        with self.settings(COMPANY_INVOICE_INCLUDE_VAT=True):
            context = self.charge._get_template_context()
            self.assertTrue(context.get('include_vat'))
            self.assertIn('vat', context)
            self.assertIn('vat_value', context)

            # TODO: check vat value

        # generate invoice & invoice items
        self.charge.invoice = mommy.make(Invoice)
        items = mommy.make(InvoiceItem, invoice=self.charge.invoice,
                           currency='chf', _quantity=2)

        context = self.charge._get_template_context()
        self.assertEqual(len(context.get('invoice_items')), len(items))
        self.assertEqual(context.get('currency'), 'chf')

        # check currency from items (instead of fallback)
        with self.settings(DJSTRIPE_CURRENCIES=(('usd', 'US Dollar'),)):
            context = self.charge._get_template_context()
            self.assertEqual(context.get('currency'), 'chf')


class InvoiceTweakTestCase(StripeTestCaseMixin, TestCase):

    TEST_DIR = os.path.join(tempfile.gettempdir(), '.dargtests')
    COMPANY_INVOICES_ROOT = os.path.join(TEST_DIR, 'invoices')

    @classmethod
    def setUpClass(cls):
        super(InvoiceTweakTestCase, cls).setUpClass()

        cls._test_logging_handler = TestLoggingHandler(level='DEBUG')
        # logger.addHandler(cls._test_logging_handler)
        logger.handlers = [cls._test_logging_handler]
        cls._log_messages = cls._test_logging_handler.messages

    @classmethod
    def tearDownClass(cls):
        super(InvoiceTweakTestCase, cls).tearDownClass()

        # remove tempdir
        shutil.rmtree(cls.TEST_DIR)

    def setUp(self):
        super(InvoiceTweakTestCase, self).setUp()

        # reset test log handler for each test
        self._test_logging_handler.reset()

        self.invoice = mommy.make(Invoice)

    @override_settings(COMPANY_INVOICES_ROOT=COMPANY_INVOICES_ROOT)
    @patch('utils.pdf.render_pdf')
    def test_generate_invoice_pdf(self, mock_render_pdf):

        # create subscriber
        subscriber = mommy.make(settings.DJSTRIPE_SUBSCRIBER_MODEL)
        self.invoice.customer.subscriber = subscriber

        # test pdf exists (and not override_existing)
        test_filepath = os.path.join(
            os.path.dirname(__file__), 'files', 'example.pdf')

        with patch.object(self.invoice, '_get_pdf_filepath',
                          return_value=test_filepath):
            pdf_filepath = self.invoice._generate_invoice_pdf()
            self.assertEqual(pdf_filepath, test_filepath)

        # test error logging when no address
        self.assertEqual(len(self._log_messages.get('error')), 1)
        self._test_logging_handler.reset()

        # test pdf generation failed
        mock_render_pdf.return_value = False
        mock_render_pdf.side_effect = ValueError()
        pdf_filepath = self.invoice._generate_invoice_pdf()
        self.assertIsNone(pdf_filepath)
        # test for 3 errors: no address, no pdf (2x)
        self.assertEqual(len(self._log_messages.get('error')), 3)
        self._test_logging_handler.reset()

        # mock pdf generation
        mock_render_pdf.return_value = '<PDF CONTENT>'
        mock_render_pdf.side_effect = None
        pdf_filepath = self.invoice._generate_invoice_pdf()
        self.assertTrue(os.path.exists(pdf_filepath))

        # TODO: test override_existing

    @override_settings(COMPANY_INVOICES_ROOT=COMPANY_INVOICES_ROOT)
    def test_get_invoice_pdf_dir_for_company(self):
        subscriber = mommy.make(settings.DJSTRIPE_SUBSCRIBER_MODEL)
        pdf_dir = self.invoice._get_invoice_pdf_dir_for_company(subscriber)
        self.assertIn('{}{}{}'.format(subscriber.pk, os.sep, self.invoice.pk),
                      pdf_dir)

    def test_get_pdf_filepath(self):

        with patch.object(self.invoice, '_get_invoice_pdf_dir_for_company') \
                as mock_pdf_dir:

            pdf_dir = os.path.join(__file__, 'files')
            mock_pdf_dir.return_value = pdf_dir

            pdf_path = self.invoice._get_pdf_filepath()
            self.assertIn(settings.COMPANY_INVOICE_FILENAME, pdf_path)
            self.assertIn(str(self.invoice.pk), pdf_path)
            self.assertIn(pdf_dir, pdf_path)

    def test_has_invoice_pdf(self):

        with patch.object(self.invoice, '_get_pdf_filepath') as mock_filepath:

            mock_filepath.return_value = ''
            self.assertFalse(self.invoice.has_invoice_pdf)

            mock_filepath.return_value = os.path.join(
                os.path.dirname(__file__), 'files', 'example.pdf')
            self.assertTrue(self.invoice.has_invoice_pdf)

            mock_filepath.return_value = os.path.join(
                os.path.dirname(__file__), 'files', 'missing.pdf')
            self.assertFalse(self.invoice.has_invoice_pdf)

    def test_get_template_context(self):

        # check simple stuff first
        context = self.invoice._get_template_context()
        self.assertEqual(context.get('invoice'), self.invoice)
        self.assertIn('site', context)
        self.assertIn('STATIC_URL', context)
        self.assertIn('BASE_DIR', context)
        self.assertGreater(len(context['BASE_DIR']), 3)
        self.assertIn('invoice_items', context)
        self.assertEqual(len(context.get('invoice_items')), 0)
        self.assertIn('company', context)
        self.assertIn('protocol', context)
        self.assertIn('include_vat', context)

        # no items, check fallback currency
        with self.settings(DJSTRIPE_CURRENCIES=(('usd', 'US Dollar'),)):
            context = self.invoice._get_template_context()
            self.assertEqual(context.get('currency'), 'usd')

        # check vat setting
        with self.settings(COMPANY_INVOICE_INCLUDE_VAT=False):
            context = self.invoice._get_template_context()
            self.assertFalse(context.get('include_vat'))
            self.assertNotIn('vat', context)
            self.assertNotIn('vat_value', context)

        with self.settings(COMPANY_INVOICE_INCLUDE_VAT=True):
            context = self.invoice._get_template_context()
            self.assertTrue(context.get('include_vat'))
            self.assertIn('vat', context)
            self.assertIn('vat_value', context)

        # generate invoice items
        items = mommy.make(InvoiceItem, invoice=self.invoice, currency='chf',
                           _quantity=2)

        context = self.invoice._get_template_context()
        self.assertEqual(len(context.get('invoice_items')), len(items))
        self.assertEqual(context.get('currency'), 'chf')

        # check currency from items (instead of fallback)
        with self.settings(DJSTRIPE_CURRENCIES=(('usd', 'US Dollar'),)):
            context = self.invoice._get_template_context()
            self.assertEqual(context.get('currency'), 'chf')
