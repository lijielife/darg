
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

        cmd.handle()
        mock_generate_invoice_pdf.assert_not_called()

        options = {'invoice_id': [-1]}
        cmd.handle(**options)
        mock_generate_invoice_pdf.assert_not_called()

        invoice = mommy.make(Invoice)
        options['invoice_id'].append(invoice.pk)
        cmd.handle(**options)
        mock_generate_invoice_pdf.assert_called()
