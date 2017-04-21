
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.test import TestCase, RequestFactory

from project.generators import OperatorGenerator, UserGenerator
from project.tests.mixins import StripeTestCaseMixin, SubscriptionTestMixin

from ..middleware import CompanySubscriptionRequired, resolve_url


class CompanySubscriptionRequiredTestCase(StripeTestCaseMixin,
                                          SubscriptionTestMixin,
                                          TestCase):

    def setUp(self):
        super(CompanySubscriptionRequiredTestCase, self).setUp()

        self.middleware = CompanySubscriptionRequired()

        factory = RequestFactory()

        whitelist_url = '/start/'
        self.whitelist_req = factory.get(whitelist_url)
        blacklist_url = self.middleware.BLACKLIST_URLS[0].replace('^', '/')
        self.blacklist_req = factory.get(blacklist_url)

        self.anonymous_user = AnonymousUser()
        self.user = UserGenerator().generate()
        self.operator = OperatorGenerator().generate()

    def test_process_request(self):

        # check whitelisted url for anonymous user
        req = self.whitelist_req
        req.user = self.anonymous_user
        res = self.middleware.process_request(req)
        self.assertIsNone(res)

        # check blacklisted url for anonymous user
        req = self.blacklist_req
        req.user = self.anonymous_user
        res = self.middleware.process_request(req)
        self.assertIsNone(res)

        # check whitelisted url for authenticated user (no operator)
        req = self.whitelist_req
        req.user = self.user
        res = self.middleware.process_request(req)
        self.assertIsNone(res)

        # check blacklisted url for authenticated user (no operator)
        req = self.blacklist_req
        req.user = self.user
        res = self.middleware.process_request(req)
        self.assertIsNone(res)

        # check whitelisted url for operator user
        req = self.whitelist_req
        req.user = self.operator.user
        res = self.middleware.process_request(req)
        self.assertIsNone(res)

        # check blacklisted url for operator user
        req = self.blacklist_req
        req.user = self.operator.user
        res = self.middleware.process_request(req)
        self.assertIsNotNone(res)
        self.assertTrue(isinstance(res, HttpResponseRedirect))
        self.assertEqual(
            res.url,
            resolve_url('djstripe:subscribe',
                        **dict(company_id=self.operator.company_id))
        )

        # add subscription
        self.add_subscription(self.operator.company)

        # req = self.blacklist_req
        # req.user = self.operator.user
        res = self.middleware.process_request(req)
        self.assertIsNone(res)
