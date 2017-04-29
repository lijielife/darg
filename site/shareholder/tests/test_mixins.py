import datetime

import mock
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase, Client
from django.utils import timezone
from model_mommy import mommy, random_gen

from project.generators import (CompanyGenerator, OperatorGenerator,
                                OptionTransactionGenerator, PositionGenerator,
                                ShareholderGenerator, UserGenerator)

from ..mixins import (AuthTokenLoginViewMixin,
                      DiscountedTaxByVestingModelMixin,
                      ShareholderStatementReportViewMixin)
from ..models import Country, ShareholderStatementReport
from utils.session import add_company_to_session


class AuthTokenLoginViewMixinTestCase(TestCase):

    def setUp(self):
        super(AuthTokenLoginViewMixinTestCase, self).setUp()

        self.factory = RequestFactory()
        self.mixin = AuthTokenLoginViewMixin()
        self.mixin.http_method_names = []

    @mock.patch('shareholder.mixins.auth_decorators.login_required')
    @mock.patch('shareholder.mixins.logout')
    @mock.patch('shareholder.mixins.login')
    def test_dispatch(self, mock_login, mock_logout, mock_login_required):

        self.mixin.http_method_not_allowed = mock.Mock(side_effect=Exception)

        req = self.factory.get('/')

        with self.assertRaises(Exception):
            self.mixin.dispatch(req)
            self.mixin.http_method_not_allowed.assert_called()
            self.mixin.http_method_not_allowed.reset_mock()

        self.mixin.http_method_names = ['get']
        self.mixin.get = mock.Mock()

        self.mixin.dispatch(req)
        self.mixin.get.assert_called()
        self.mixin.get.reset_mock()

        user = UserGenerator().generate()
        user.is_active = False
        user.save()

        req = self.factory.get('/', data=dict(token=user.auth_token))
        self.mixin.dispatch(req)
        mock_logout.assert_called()
        mock_logout.reset_mock()

        user.is_active = True
        user.save()

        self.mixin.dispatch(req)
        mock_login.assert_called()
        mock_login.reset_mock()

        self.mixin.login_user = False
        self.mixin.dispatch(req)
        mock_login.assert_not_called()

        self.mixin.login_required = True
        self.mixin.dispatch(req)
        mock_login_required.assert_called()


class AddressModelMixinTestCase(TestCase):

    def setUp(self):
        super(AddressModelMixinTestCase, self).setUp()

        self.company = CompanyGenerator().generate()

    def test_has_address(self):
        self.assertFalse(self.company.has_address)

        self.company.REQUIRED_ADDRESS_FIELDS = []
        self.assertTrue(self.company.has_address)

        self.company.REQUIRED_ADDRESS_FIELDS = ['street']
        self.assertFalse(self.company.has_address)
        self.company.street = random_gen.gen_string(10)
        self.assertTrue(self.company.has_address)

    def test_read_address_from_stripe_object(self):

        stripe_data = dict()
        self.company.read_address_from_stripe_object(stripe_data)
        self.assertFalse(bool(self.company.street))

        stripe_data = {
            'address_line1': random_gen.gen_string(10),
            'address_line2': random_gen.gen_string(8),
            'address_zip': random_gen.gen_string(5),
            'address_city': random_gen.gen_string(6),
            'address_state': random_gen.gen_string(10)
        }
        self.company.read_address_from_stripe_object(stripe_data, save=False)
        self.assertEqual(self.company.street, stripe_data['address_line1'])
        self.assertEqual(self.company.street2, stripe_data['address_line2'])
        self.assertEqual(self.company.postal_code, stripe_data['address_zip'])
        self.assertEqual(self.company.city, stripe_data['address_city'])
        self.assertEqual(self.company.province, stripe_data['address_state'])

        self.company.refresh_from_db()
        self.assertFalse(bool(self.company.street))
        self.assertFalse(bool(self.company.street2))
        self.assertFalse(bool(self.company.postal_code))
        self.assertFalse(bool(self.company.city))
        self.assertFalse(bool(self.company.province))

        # check country
        stripe_data.update(dict(address_country='__foo__'))
        self.company.read_address_from_stripe_object(stripe_data)

        self.company.refresh_from_db()
        self.assertFalse(bool(self.company.country))
        self.assertTrue(bool(self.company.street))
        self.assertTrue(bool(self.company.street2))
        self.assertTrue(bool(self.company.postal_code))
        self.assertTrue(bool(self.company.city))
        self.assertTrue(bool(self.company.province))

        stripe_data.update(dict(
            address_country=Country.objects.first().name.lower()
        ))
        self.company.read_address_from_stripe_object(stripe_data)
        self.assertTrue(bool(self.company.country))


class DiscountedTaxByVestingModelMixinTestCase(TestCase):

    def setUp(self):
        self.shareholder = ShareholderGenerator().generate()
        self.company = self.shareholder.company
        self.position = PositionGenerator().generate(
            buyer=self.shareholder, count=30, vesting_months=24)
        self.option = OptionTransactionGenerator().generate(
            buyer=self.shareholder, count=16, vesting_months=120)
        self.mixin = DiscountedTaxByVestingModelMixin()

    def test_get_vesting_expires_at(self):
        """ return date when vesting expires """
        today = timezone.now().date()
        self.assertEqual(
            self.position.get_vesting_expires_at(),
            today + relativedelta(years=2))
        self.assertEqual(
            self.option.get_vesting_expires_at(),
            today + relativedelta(years=10))

    def test_get_discounted_tax_ratio(self):
        """ return percent to be applied for discounted tax value calculation
        read: https://goo.gl/n5p0IR
        """
        passed_date = timezone.make_aware(datetime.datetime(2013, 1, 1)).date()
        future_date = timezone.now().date() + relativedelta(years=1)

        self.assertEqual(self.position.get_discounted_tax_ratio(), 0.89)
        self.assertEqual(self.position.get_discounted_tax_ratio(
            date=passed_date), 0)
        self.assertEqual(self.position.get_discounted_tax_ratio(
            date=future_date), 0.9434)

        self.assertEqual(self.option.get_discounted_tax_ratio(), 0.55839)
        self.assertEqual(self.option.get_discounted_tax_ratio(
            date=passed_date), 0)
        self.assertEqual(self.option.get_discounted_tax_ratio(
            date=future_date), 0.5919)

    def test_get_discounted_tax_value(self):
        """ return value to be used for discounted tax """
        self.assertEqual(self.position.get_discounted_tax_value(),
                         2670)
        self.assertEqual(self.option.get_discounted_tax_value(), 893.424)


class ShareholderStatementReportViewMixinTestCase(TestCase):

    def setUp(self):
        super(ShareholderStatementReportViewMixinTestCase, self).setUp()

        self.factory = RequestFactory()
        self.mixin = ShareholderStatementReportViewMixin()
        self.mixin.request = self.factory.get('/')

        self.client = Client()

    def test_get_queryset(self):
        self.mixin.get_company_pks = mock.Mock(return_value=[])

        with self.assertRaises(ValueError):
            self.mixin.get_queryset()

        company = CompanyGenerator().generate()
        add_company_to_session(self.client.session, company)
        self.mixin.request.session = self.client.session
        report = mommy.make(ShareholderStatementReport, company=company)

        self.mixin.get_company_pks.return_value = [company.pk]

        queryset = self.mixin.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertIn(report, queryset)
