#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import copy

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse, NoReverseMatch, resolve
from django.http import Http404
from django.test import TestCase, Client, modify_settings, RequestFactory
from django.utils.translation import gettext as _

import mock

from djstripe import settings as djstripe_settings
from djstripe.models import Invoice
from model_mommy import mommy, random_gen
from stripe import StripeError
from two_factor.admin import AdminSiteOTPRequiredMixin

from shareholder.models import Company
from project.generators import (
    CompanyGenerator, SecurityGenerator,
    OperatorGenerator, DEFAULT_TEST_DATA, UserGenerator)
from project.tests.mixins import StripeTestCaseMixin, SubscriptionTestMixin

from ..views import (SubscriptionsListView, AccountView, ChangeCardView,
                     ConfirmFormView, ChangePlanView, SyncHistoryView,
                     SubscribeView, InvoiceDetailView)


class CompanyAdminDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = CompanyGenerator().generate()
        self.user = UserGenerator().generate()

    # disable two-factor authentication
    @modify_settings(MIDDLEWARE_CLASSES={
        'remove': ['django_otp.middleware.OTPMiddleware']
    })
    @mock.patch.object(AdminSiteOTPRequiredMixin, 'has_permission',
                       return_value=True)
    def test_view(self, mock_permission):

        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.client.force_login(self.user)

        res = self.client.get(reverse('admin:shareholder_company_change',
                                      args=[self.company.pk]))

        self.assertEqual(res.status_code, 200)


class CompanyDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_numbered_shares(self):

        company = CompanyGenerator().generate()
        SecurityGenerator().generate(
            company=company, track_numbers=True)
        operator = OperatorGenerator().generate(company=company)

        self.client.login(username=operator.user.username,
                          password=DEFAULT_TEST_DATA.get('password'))

        res = self.client.get(reverse(
            'company', kwargs={'company_id': company.id}))

        self.assertEqual(res.status_code, 200)
        self.assertIn(
            _('tracking security numbers for owners enabled. segments:'),
            res.content)


class SubscriptionsListViewTestCase(TestCase):

    def setUp(self):
        super(SubscriptionsListViewTestCase, self).setUp()

        self.factory = RequestFactory()
        self.view = SubscriptionsListView()
        self.view.kwargs = dict()

    def test_get_queryset(self):
        self.view.request = self.factory.get('/')

        # non-operator
        self.view.request.user = UserGenerator().generate()
        self.assertEqual(len(self.view.get_queryset()), 0)

        # operator
        self.view.request.user = OperatorGenerator().generate().user
        self.assertEqual(len(self.view.get_queryset()), 1)

    def test_get(self):

        # mock get_queryset
        self.view.get_queryset = mock.Mock(return_value=Company.objects.none())

        operator = OperatorGenerator().generate()

        self.view.request = self.factory.get('/')
        self.view.request.user = operator.user

        with self.assertRaises(Http404):
            self.view.get(self.view.request)

        self.view.get_queryset = mock.Mock(return_value=Company.objects.filter(
            pk=operator.company_id))

        res = self.view.get(self.view.request)
        self.assertEqual(res.status_code, 302)  # redirect

        # add another company/operator to user
        operator2 = OperatorGenerator().generate(user=operator.user)
        self.view.get_queryset = mock.Mock(return_value=Company.objects.filter(
            pk__in=[operator.company_id, operator2.company_id]))

        res = self.view.get(self.view.request)
        self.assertEqual(res.status_code, 200)

        # test allow_empty False
        self.view.allow_empty = False
        self.view.get_paginate_by = mock.Mock(return_value=True)
        with mock.patch.object(self.view, 'get_queryset',
                               return_value=Company.objects.none()):
            with self.assertRaises(Http404):
                self.view.get(self.view.request)


class AccountViewTestCase(StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(AccountViewTestCase, self).setUp()

        self.view = AccountView()

    @mock.patch('djstripe.views.AccountView.get_context_data')
    def test_get_context_data(self, mock_get_context_data):

        operator = OperatorGenerator().generate()
        customer = operator.company.get_customer()
        plans = []
        payment_plans = copy.deepcopy(settings.DJSTRIPE_PLANS)
        for plan in payment_plans:
            payment_plans[plan]['plan'] = plan
            plans.append(payment_plans[plan])

        mock_get_context_data.return_value = dict(
            customer=customer, plans=plans)

        context = self.view.get_context_data()
        self.assertIn('customer', context)
        self.assertIn('plans', context)

        plan = context.get('plans')[0]
        self.assertNotIn('unsubscribable', plan)

        customer.subscriber.can_subscribe_plan = mock.Mock(return_value=False)
        context = self.view.get_context_data()
        plan = context.get('plans')[0]
        self.assertTrue(plan.get('unsubscribable'))


class ChangeCardViewTestCase(TestCase):

    def setUp(self):
        super(ChangeCardViewTestCase, self).setUp()

        self.view = ChangeCardView()
        self.view.kwargs = dict()

    def test_get_post_success_url(self):

        with self.assertRaises(NoReverseMatch):
            self.view.get_post_success_url()

        company = CompanyGenerator().generate()
        self.view.kwargs.update(dict(company_id=company.pk))

        self.assertIn(str(company.pk), self.view.get_post_success_url())


class ConfirmFormViewTestCase(StripeTestCaseMixin, SubscriptionTestMixin,
                              TestCase):

    def setUp(self):
        super(ConfirmFormViewTestCase, self).setUp()

        self.factory = RequestFactory()
        self.view = ConfirmFormView()
        self.view.kwargs = dict()

    def test_get(self):

        company = CompanyGenerator().generate()
        customer = company.get_customer()
        self.assertEqual(customer.subscriber, company)
        operator = OperatorGenerator().generate(company=company)

        view_url = reverse('djstripe:confirm',
                           args=[operator.company_id, 'test'])
        subscribe_url = reverse('djstripe:subscribe', args=[company.pk])

        req = self.factory.get(view_url)
        req.user = operator.user
        req.resolver_match = resolve(view_url)
        view_kwargs = dict(company_id=operator.company_id)
        self.view.request = req

        res = self.view.get(req, **view_kwargs)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, subscribe_url)

        # test success
        self.view.kwargs = dict(plan='test')

        res = self.view.get(req, **view_kwargs)
        self.assertEqual(res.status_code, 200)

        # test already subscribed
        self.add_subscription(company)

        res = self.view.get(req, **view_kwargs)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, subscribe_url)

    @mock.patch('djstripe.views.ConfirmFormView.get_context_data')
    def test_get_context_data(self, mock_get_context_data):
        operator = OperatorGenerator().generate()
        customer = operator.company.get_customer()
        plan = djstripe_settings.PAYMENT_PLANS['test']

        mock_get_context_data.return_value = dict(customer=customer, plan=plan)

        context = self.view.get_context_data()
        self.assertIn('customer', context)
        self.assertIn('plan', context)

        with mock.patch.object(customer.subscriber, 'validate_plan',
                               return_value=(True, [])):
            context = self.view.get_context_data()
            self.assertNotIn('plan_unsubscribable', context)
            self.assertNotIn('plan_errors', context)

        with mock.patch.object(customer.subscriber, 'validate_plan',
                               return_value=(False, ['error'])):
            context = self.view.get_context_data()
            self.assertIn('plan_unsubscribable', context)
            self.assertIn('plan_errors', context)

    @mock.patch('djstripe.models.Customer.sync_card')
    @mock.patch('utils.subscriptions.stripe_company_shareholder_invoice_item')
    @mock.patch('utils.subscriptions.stripe_company_security_invoice_item')
    def test_post(self, mock_security_invoice_item,
                  mock_shareholder_invoice_item, mock_sync_card):
        operator = OperatorGenerator().generate()
        operator.company.get_customer()

        view_url = reverse('djstripe:confirm',
                           args=[operator.company_id, 'test'])

        req = self.factory.post(view_url)
        req.user = operator.user
        req.resolver_match = resolve(view_url)
        self.view.request = req
        self.view.kwargs = dict(plan='test', company_id=operator.company_id)

        self.view.form_invalid = mock.Mock(
            side_effect=ValidationError('ERROR'))
        with self.assertRaises(ValidationError):
            res = self.view.post(req)
            self.assertIn('ERROR', res.content)  # pragma: nocover

        post_data = dict(plan='test', email=random_gen.gen_email())
        req = self.factory.post(view_url, data=post_data)
        req.user = operator.user
        req.resolver_match = resolve(view_url)
        self.view.request = req

        with mock.patch('djstripe.models.Customer.subscribe'):
            res = self.view.post(req)
            self.assertEqual(res.status_code, 302)

        mock_shareholder_invoice_item.assert_called()
        mock_security_invoice_item.assert_called()

        company = operator.company.__class__.objects.get(
            pk=operator.company_id)
        self.assertEqual(company.email, post_data['email'])

        # test unsubscribable
        with mock.patch('shareholder.models.Company.validate_plan',
                        return_value=(False, [])):

            with self.assertRaises(ValidationError):
                self.view.post(req)

        with mock.patch('djstripe.models.Customer.subscribe',
                        side_effect=StripeError('STRIPEERROR')):
            with self.assertRaises(ValidationError):
                res = self.view.post(req)
                self.assertIn('STRIPEERROR', res.content)  # pragma: nocover

    def test_get_success_url(self):
        with self.assertRaises(NoReverseMatch):
            self.view.get_success_url()

        self.view.kwargs = dict(company_id=1)
        self.assertEqual(self.view.get_success_url(),
                         reverse('djstripe:history', args=[1]))


class ChangePlanViewTestCase(StripeTestCaseMixin, SubscriptionTestMixin,
                             TestCase):

    def setUp(self):
        super(ChangePlanViewTestCase, self).setUp()

        self.factory = RequestFactory()
        self.view = ChangePlanView()
        self.view.kwargs = dict()

    @mock.patch('djstripe.models.Customer.sync_card')
    @mock.patch('utils.subscriptions.stripe_company_shareholder_invoice_item')
    @mock.patch('utils.subscriptions.stripe_company_security_invoice_item')
    def test_post(self, mock_security_invoice_item,
                  mock_shareholder_invoice_item, mock_sync_card):
        operator = OperatorGenerator().generate()

        view_url = reverse('djstripe:confirm',
                           args=[operator.company_id, 'test'])

        req = self.factory.post(view_url)
        req.user = operator.user
        req.resolver_match = resolve(view_url)
        self.view.request = req
        self.view.kwargs = dict(plan='test', company_id=operator.company_id)

        self.view.form_invalid = mock.Mock(
            side_effect=ValidationError('ERROR'))

        # no customer
        with self.assertRaises(ValidationError):
            res = self.view.post(req)
            self.assertIn('ERROR', res.content)  # pragma: nocover

        # create customer
        operator.company.get_customer()

        with self.assertRaises(ValidationError):
            self.view.post(req)
            self.assertIn('ERROR', res.content)  # pragma: nocover

        post_data = dict(plan='test')
        req = self.factory.post(view_url, data=post_data)
        req.user = operator.user
        req.resolver_match = resolve(view_url)
        self.view.request = req

        with mock.patch('djstripe.models.Customer.subscribe'):
            res = self.view.post(req)
            self.assertEqual(res.status_code, 302)

        mock_shareholder_invoice_item.assert_called()
        mock_security_invoice_item.assert_called()

        # test prorate
        self.add_subscription(operator.company)
        with mock.patch('djstripe.models.Customer.subscribe') as mock_sub:
            with mock.patch('company.views.PRORATION_POLICY_FOR_UPGRADES',
                            return_value=False):
                self.view.post(req)
                mock_sub.assert_called_with('test', prorate=False)

            mock_sub.reset_mock()

            with mock.patch('company.views.PRORATION_POLICY_FOR_UPGRADES',
                            return_value=True):
                self.view.post(req)
                mock_sub.assert_called_with('test', prorate=False)

            mock_sub.reset_mock()

            with mock.patch('company.views.PRORATION_POLICY_FOR_UPGRADES',
                            return_value=True):
                plans = copy.deepcopy(settings.DJSTRIPE_PLANS)
                plans['test']['price'] = 1
                with self.settings(DJSTRIPE_PLANS=plans):
                    self.view.post(req)
                    mock_sub.assert_called_with('test', prorate=True)

        # test unsubscribable
        with mock.patch('shareholder.models.Company.validate_plan',
                        return_value=(False, [])):

            with self.assertRaises(ValidationError):
                self.view.post(req)

        with mock.patch('djstripe.models.Customer.subscribe',
                        side_effect=StripeError('STRIPEERROR')):
            with self.assertRaises(ValidationError):
                res = self.view.post(req)
                self.assertIn('STRIPEERROR', res.content)  # pragma: nocover

    def test_get_success_url(self):
        with self.assertRaises(NoReverseMatch):
            self.view.get_success_url()

        self.view.kwargs = dict(company_id=1)
        self.assertEqual(self.view.get_success_url(),
                         reverse('djstripe:history', args=[1]))


class SyncHistoryViewTestCase(StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(SyncHistoryViewTestCase, self).setUp()

        self.factory = RequestFactory()
        self.view = SyncHistoryView()

    @mock.patch('company.views.sync_subscriber')
    def test_post(self, mock_sync_subscriber):

        company = CompanyGenerator().generate()
        customer = company.get_customer()

        url = reverse('djstripe:sync_history', args=[company.pk])
        req = self.factory.post(url)
        req.resolver_match = resolve(url)

        mock_sync_subscriber.return_value = customer

        with mock.patch('company.views.render') as mock_render:
            self.view.post(req)
            mock_render.assert_called_with(req, self.view.template_name,
                                           dict(customer=customer))


class SubscribeViewTestCase(StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(SubscribeViewTestCase, self).setUp()

        self.view = SubscribeView()

    @mock.patch('djstripe.views.SubscribeView.get_context_data')
    def test_get_context_data(self, mock_get_context_data):

        company = CompanyGenerator().generate()
        customer = company.get_customer()

        # FIXME: somehow, settings can be modified
        plans = copy.deepcopy(settings.DJSTRIPE_PLANS)
        if 'unsubscribable' in plans['test']:
            del plans['test']['unsubscribable']
        mock_get_context_data.return_value = dict(
            customer=customer,
            PAYMENT_PLANS=plans
        )

        with mock.patch.object(customer.subscriber, 'validate_plan',
                               return_value=(True, [])):
            context = self.view.get_context_data()
            self.assertNotIn('unsubscribable',
                             context['PAYMENT_PLANS']['test'])

        with mock.patch.object(customer.subscriber, 'validate_plan',
                               return_value=(False, [])):
            context = self.view.get_context_data()
            self.assertIn('unsubscribable', context['PAYMENT_PLANS']['test'])
            self.assertTrue(context['PAYMENT_PLANS']['test']['unsubscribable'])


class InvoiceDetailViewTestCase(StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(InvoiceDetailViewTestCase, self).setUp()

        self.factory = RequestFactory()
        self.view = InvoiceDetailView()
        self.view.kwargs = dict()

    def test_get_queryset(self):

        self.assertEqual(len(self.view.get_queryset()), 0)

        company = mommy.make(Company)
        customer = company.get_customer()

        self.view.kwargs.update(dict(company_id=company.pk))
        self.assertEqual(len(self.view.get_queryset()), 0)

        mommy.make(Invoice, customer=customer, _quantity=2)
        self.assertEqual(len(self.view.get_queryset()), 2)

    @mock.patch('company.views.sendfile')
    def test_get(self, mock_sendfile):

        req = self.factory.get('/')

        self.view.kwargs.update(dict(pk=0))

        with self.assertRaises(Http404):
            self.view.get(req)

        invoice = mommy.make(Invoice)
        invoice._get_pdf_filepath = mock.Mock()
        invoice._get_pdf_filepath.return_value = os.path.join(
            os.path.dirname(__file__), 'files', 'example.pdf')
        self.view.get_object = mock.Mock(return_value=invoice)

        self.view.get(req)
        mock_sendfile.assert_called()

        # check invoice generation
        invoice._generate_invoice_pdf = mock.Mock()
        invoice._get_pdf_filepath.return_value = ''

        with self.assertRaises(Http404):
            self.view.get(req)

        invoice._generate_invoice_pdf.assert_called()
