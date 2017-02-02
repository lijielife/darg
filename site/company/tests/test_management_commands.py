
from django.test import TestCase

import mock

from djstripe.models import Invoice
from model_mommy import mommy

from ..management.commands.generate_invoice_pdf import (
    Command as GenerateInvoicePDFCommand
)


class GenerateInvoicePDFManagementCommandTestCase(TestCase):

    @mock.patch.object(Invoice, '_generate_invoice_pdf')
    def test_handle(self, mock_generate_invoice_pdf):
        cmd = GenerateInvoicePDFCommand()

        global called
        called = 0

        def _side_effect(override_existing=False):
            globals()['called'] += 1

        mock_generate_invoice_pdf.side_effect = _side_effect

        cmd.handle()
        self.assertEqual(called, 0)

        options = {'invoice_id': [-1]}
        cmd.handle(**options)
        self.assertEqual(called, 0)

        invoice = mommy.make(Invoice)
        options['invoice_id'].append(invoice.pk)
        cmd.handle(**options)
        self.assertEqual(called, 1)
