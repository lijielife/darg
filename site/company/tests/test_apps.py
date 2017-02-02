
import os
import shutil
import tempfile

from unittest import skip as skip_test

from django.conf import settings
from django.test import TestCase

from djstripe.models import Charge, Invoice, InvoiceItem
from mock import patch
from model_mommy import mommy

from project.tests.mixins import StripeTestCaseMixin
from shareholder.models import Company


class ChargeTweakTestCase(StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(ChargeTweakTestCase, self).setUp()

        self.charge = mommy.make(Charge)

    @skip_test('NotImplemented')
    def test_send_receipt(self):
        pass

    @skip_test('NotImplemented')
    def test_get_customer_data(self):
        pass

    @skip_test('NotImplemented')
    def test_get_template_context(self):
        pass


class InvoiceTweakTestCase(StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(InvoiceTweakTestCase, self).setUp()

        self.invoice = mommy.make(Invoice)

    @skip_test('NotImplemented')
    def test_generate_invoice_pdf(self):
        pass

    def test_get_invoice_pdf_dir_for_company(self):
        tempdir = tempfile.gettempdir()
        invoices_base_root = os.path.join(tempdir, '.dargtests')
        invoices_root = os.path.join(invoices_base_root, 'invoices')
        company = mommy.make(Company)
        with self.settings(COMPANY_INVOICES_ROOT=invoices_root):
            pdf_dir = self.invoice._get_invoice_pdf_dir_for_company(company)
            self.assertIn('{}{}{}'.format(company.pk, os.sep, self.invoice.pk),
                          pdf_dir)

        shutil.rmtree(invoices_base_root)

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
