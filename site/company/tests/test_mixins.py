
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import Http404, QueryDict
from django.test import TestCase, RequestFactory

from mock import Mock
from model_mommy import mommy

from project.generators import (CompanyGenerator, OperatorGenerator,
                                UserGenerator, Company)
from project.tests.mixins import StripeTestCaseMixin, SubscriptionTestMixin

from ..mixins import (SubscriptionViewCompanyObjectMixin,
                      CompanyOperatorPermissionRequiredViewMixin,
                      SubscriptionMixin, SubscriptionViewMixin)


class SubscriptionViewCompanyObjectMixinTestCase(TestCase):

    def setUp(self):
        super(SubscriptionViewCompanyObjectMixinTestCase, self).setUp()

        self.mixin = SubscriptionViewCompanyObjectMixin()
        self.mixin.kwargs = dict()

    def test_get_company(self):

        with self.assertRaises(Http404):
            self.mixin.get_company()

        self.mixin.kwargs.update(dict(company_id=0))

        with self.assertRaises(Http404):
            self.mixin.get_company()

        company = CompanyGenerator().generate()

        self.mixin.kwargs.update(dict(company_id=company.pk))
        result = self.mixin.get_company()
        self.assertIsNotNone(result)
        self.assertEqual(result, company)


class CompanyOperatorPermissionRequiredViewMixinTestCase(TestCase):

    def setUp(self):
        super(CompanyOperatorPermissionRequiredViewMixinTestCase, self).setUp()

        self.factory = RequestFactory()
        self.mixin = CompanyOperatorPermissionRequiredViewMixin()

    def test_dispatch(self):
        req = self.factory.get('/')

        # test authentication
        req.user = AnonymousUser()
        res = self.mixin.dispatch(req)
        self.assertEqual(res.status_code, 302)

        operator = OperatorGenerator().generate()
        # mock mixin.get_company
        self.mixin.get_company = Mock(return_value=operator.company)

        req.user = UserGenerator().generate()
        res = self.mixin.dispatch(req)
        self.assertEqual(res.status_code, 302)

        # check company operator
        res = self.mixin.dispatch(req)
        self.assertEqual(res.status_code, 302)

        # set operator user
        req.user = operator.user
        # expecting "success": 'super' object has no attribute 'dispatch'
        with self.assertRaises(AttributeError):
            self.mixin.dispatch(req)


class SubscriptionMixinTestCase(StripeTestCaseMixin, SubscriptionTestMixin,
                                TestCase):

    def setUp(self):
        super(SubscriptionMixinTestCase, self).setUp()

        self.mixin = SubscriptionMixin()

    def test_check_subscription(self):

        with self.assertRaises(ValueError):
            self.mixin.check_subscription(None)

        company = CompanyGenerator().generate()

        self.assertFalse(self.mixin.check_subscription(company))

        # add subscription
        self.add_subscription(company)

        self.assertTrue(self.mixin.check_subscription(company))

        features = 'test'
        self.assertFalse(self.mixin.check_subscription(company, features))

        plan_name = company.get_current_subscription_plan()
        features = settings.DJSTRIPE_PLANS[plan_name]['features'].keys()
        self.assertTrue(self.mixin.check_subscription(company, features))

        # check iterable
        features = features[0]
        self.assertTrue(self.mixin.check_subscription(company, features))


class SubscriptionViewMixinTestCase(StripeTestCaseMixin, SubscriptionTestMixin,
                                    TestCase):

    def setUp(self):
        super(SubscriptionViewMixinTestCase, self).setUp()

        self.mixin = SubscriptionViewMixin()
        self.mixin.request = RequestFactory().get('/')
        self.mixin.request.user = AnonymousUser()

    def test_get_user_companies(self):

        with self.assertRaises(NotImplementedError):
            self.mixin.get_user_companies()

    def test_get_company_pks(self):

        # mock get_user_companies
        self.mixin.get_user_companies = Mock(return_value=[])

        self.assertEqual(self.mixin.get_company_pks(), [])

        companies = mommy.make(Company, _quantity=3)
        company_pks = [company.pk for company in companies]
        self.mixin.get_user_companies = Mock(
            return_value=Company.objects.filter(pk__in=company_pks))

        self.assertEqual(self.mixin.get_company_pks(), [])

        # add subscription
        self.add_subscription(companies[0])

        self.assertEqual(self.mixin.get_company_pks(), [company_pks[0]])

        # check features
        self.mixin.subscription_features = ['foo']
        self.assertEqual(self.mixin.get_company_pks(), [])

        # check query params
        self.mixin.subscription_features = []
        self.mixin.request.query_params = QueryDict(
            '{}={}'.format(self.mixin.COMPANY_QUERY_VAR, company_pks[0]))
        self.assertEqual(self.mixin.get_company_pks(), [company_pks[0]])

        self.mixin.request.query_params = QueryDict(
            '{}={}'.format(self.mixin.COMPANY_QUERY_VAR, company_pks[1]))
        self.assertEqual(self.mixin.get_company_pks(), [])

        self.mixin.request.query_params = QueryDict(
            '{}={}'.format(self.mixin.COMPANY_QUERY_VAR, 'foo'))
        self.assertEqual(self.mixin.get_company_pks(), [])

        # if empty, consider as not set
        self.mixin.request.query_params = QueryDict(
            '{}={}'.format(self.mixin.COMPANY_QUERY_VAR, ''))
        self.assertEqual(self.mixin.get_company_pks(), [company_pks[0]])
