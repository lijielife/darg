
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory

import mock
from model_mommy import mommy, random_gen

from project.generators import (CompanyGenerator, UserGenerator,
                                OperatorGenerator)
from ..models import Country, Company, ShareholderStatementReport

from ..mixins import (AuthTokenLoginViewMixin,
                      ShareholderStatementReportViewMixin)


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

        db_company = Company.objects.get(pk=self.company.pk)
        self.assertFalse(bool(db_company.street))
        self.assertFalse(bool(db_company.street2))
        self.assertFalse(bool(db_company.postal_code))
        self.assertFalse(bool(db_company.city))
        self.assertFalse(bool(db_company.province))

        # check country
        stripe_data.update(dict(address_country='__foo__'))
        self.company.read_address_from_stripe_object(stripe_data)

        db_company = Company.objects.get(pk=self.company.pk)
        self.assertFalse(bool(db_company.country))
        self.assertTrue(bool(db_company.street))
        self.assertTrue(bool(db_company.street2))
        self.assertTrue(bool(db_company.postal_code))
        self.assertTrue(bool(db_company.city))
        self.assertTrue(bool(db_company.province))

        stripe_data.update(dict(
            address_country=Country.objects.first().name.lower()
        ))
        self.company.read_address_from_stripe_object(stripe_data)
        self.assertTrue(bool(self.company.country))


class ShareholderStatementReportViewMixinTestCase(TestCase):

    def setUp(self):
        super(ShareholderStatementReportViewMixinTestCase, self).setUp()

        self.factory = RequestFactory()
        self.mixin = ShareholderStatementReportViewMixin()
        self.mixin.request = self.factory.get('/')

    def test_get_user_companies(self):
        # anonymous user
        self.mixin.request.user = AnonymousUser()
        self.assertEqual(self.mixin.get_user_companies().count(), 0)

        # auth user, but not operator
        self.mixin.request.user = UserGenerator().generate()
        self.assertEqual(self.mixin.get_user_companies().count(), 0)

        # add operator
        operator = OperatorGenerator().generate(user=self.mixin.request.user)
        company_qs = self.mixin.get_user_companies()
        self.assertEqual(company_qs.count(), 1)
        self.assertIn(operator.company, company_qs)

    def test_get_queryset(self):
        self.mixin.get_company_pks = mock.Mock(return_value=[])

        self.assertEqual(self.mixin.get_queryset().count(), 0)

        company = CompanyGenerator().generate()
        report = mommy.make(ShareholderStatementReport, company=company)

        self.mixin.get_company_pks.return_value = [company.pk]

        queryset = self.mixin.get_queryset()
        self.assertEqual(queryset.count(), 1)
        self.assertIn(report, queryset)
