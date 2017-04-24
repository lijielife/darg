
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import TestCase, RequestFactory

from mock import Mock

from project.generators import (CompanyGenerator, OperatorGenerator,
                                UserGenerator)
from project.tests.mixins import StripeTestCaseMixin, SubscriptionTestMixin

from ..mixins import (SubscriptionViewCompanyObjectMixin,
                      CompanyOperatorPermissionRequiredViewMixin,
                      SubscriptionMixin)


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
