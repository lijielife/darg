
from django.core.urlresolvers import reverse, resolve
from django.test import TestCase, RequestFactory

import mock

from project.generators import (CompanyGenerator, ShareholderGenerator,
                                SecurityGenerator)
from project.tests.mixins import StripeTestCaseMixin

from ..subscriptions import (stripe_subscriber_request_callback,
                             stripe_company_shareholder_invoice_item,
                             stripe_company_security_invoice_item)


class SubsciptionUtilsTestCase(StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(SubsciptionUtilsTestCase, self).setUp()

        self.company = CompanyGenerator().generate()

    def test_stripe_subscriber_request_callback(self):
        url = reverse('djstripe:account', args=[self.company.pk])
        req = RequestFactory().get(url)
        req.resolver_match = resolve(url)
        self.assertEqual(stripe_subscriber_request_callback(req),
                         self.company)

    @mock.patch('stripe.InvoiceItem.create')
    def test_stripe_company_shareholder_invoice_item(self,
                                                     mock_invoice_item_create):
        customer = self.company.get_customer()

        stripe_company_shareholder_invoice_item(customer, 'test', None)
        mock_invoice_item_create.assert_not_called()

        from django.conf import settings

        plans = settings.DJSTRIPE_PLANS
        plans['test']['features']['shareholders']['price'] = 10

        with self.settings(DJSTRIPE_PLANS=plans):
            stripe_company_shareholder_invoice_item(customer, 'test', None)
            mock_invoice_item_create.assert_not_called()

            shareholder_generator = ShareholderGenerator()
            shareholder_generator.generate(company=self.company)
            shareholder_generator.generate(company=self.company, number='0')

            # shareholder have no shares
            stripe_company_shareholder_invoice_item(customer, 'test', None)
            mock_invoice_item_create.assert_not_called()

            with mock.patch('shareholder.models.Shareholder.share_count',
                            return_value=10):
                stripe_company_shareholder_invoice_item(customer, 'test', None)
                mock_invoice_item_create.assert_called()
                mock_invoice_item_create.assert_called_with(
                    customer=customer.stripe_id,
                    amount=10,
                    currency=settings.DJSTRIPE_CURRENCIES[0][0],
                    invoice=None,
                    description=u'Shareholders (1 x 0.10)'
                )

    @mock.patch('stripe.InvoiceItem.create')
    def test_stripe_company_security_invoice_item(self,
                                                  mock_invoice_item_create):
        customer = self.company.get_customer()

        stripe_company_security_invoice_item(customer, 'test', None)
        mock_invoice_item_create.assert_not_called()

        from django.conf import settings

        plans = settings.DJSTRIPE_PLANS
        plans['test']['features']['securities']['price'] = 20

        with self.settings(DJSTRIPE_PLANS=plans):
            stripe_company_security_invoice_item(customer, 'test', None)
            mock_invoice_item_create.assert_not_called()

            SecurityGenerator().generate(company=self.company)

            # one security is free
            stripe_company_security_invoice_item(customer, 'test', None)
            mock_invoice_item_create.assert_not_called()

            SecurityGenerator().generate(company=self.company)

            stripe_company_security_invoice_item(customer, 'test', None)
            mock_invoice_item_create.assert_called()
            mock_invoice_item_create.assert_called_with(
                customer=customer.stripe_id,
                amount=20,
                currency=settings.DJSTRIPE_CURRENCIES[0][0],
                invoice=None,
                description=u'Extra Securities (1 x 0.20)'
            )
