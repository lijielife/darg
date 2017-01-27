#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
mixins to enhance several tests with common code
"""

import os
import sys

# from django.conf import settings
from django.db import DEFAULT_DB_ALIAS, connections
from django.test.utils import CaptureQueriesContext
from django.utils.timezone import now, timedelta

import mock
import requests
import stripe

from djstripe.models import CurrentSubscription
from model_mommy import random_gen

from .helper import FakeStripeResponse


# stolen here https://goo.gl/IdWkTr
class _AssertLessNumQueriesContext(CaptureQueriesContext):
    """ context manager to check for queries less then x """

    def __init__(self, test_case, num, connection):
        self.test_case = test_case
        self.num = num
        super(_AssertLessNumQueriesContext, self).__init__(connection)

    def __exit__(self, exc_type, exc_value, traceback):
        super(_AssertLessNumQueriesContext, self).__exit__(
            exc_type, exc_value, traceback)
        if exc_type is not None:
            return
        executed = len(self)
        # altered here from assertEqual to assertLess
        self.test_case.assertLess(
            executed, self.num,
            "%d queries executed, less then %d expected\n"
            "Captured queries were:\n%s" % (
                executed, self.num,
                '\n'.join(
                    query['sql'] for query in self.captured_queries
                )
            )
        )


class MoreAssertsTestCaseMixin(object):
    """
    some very helpfull asserts...
    """

    def assertLessNumQueries(self, num, func=None, *args, **kwargs):
        """
        ensure we do not run more queries then what's good for us
        learned here https://goo.gl/0Z8QW2
        """
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        conn = connections[using]

        context = _AssertLessNumQueriesContext(self, num, conn)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)


class FakeResponseMixin(object):
    """
    mixin to mock responses for requests calls
    """

    fake_response_content = random_gen.gen_text()

    def get_fake_response(self, method, url=None, status_code=200):
        if url is None:
            url = random_gen.gen_url()
        request = requests.Request(method=method, url=url)
        request = request.prepare()
        response = requests.Response()
        response.status_code = status_code
        response._content = self.fake_response_content
        response.request = request
        return response


class StripeTestCaseMixin(object):

    RESTORE_ATTRIBUTES = ('api_version', 'api_key')

    REQUEST_LIBRARIES = ['urlfetch', 'requests', 'pycurl']

    if sys.version_info >= (3, 0):
        REQUEST_LIBRARIES.append('urllib.request')
    else:
        REQUEST_LIBRARIES.append('urllib2')

    def setUp(self):
        super(StripeTestCaseMixin, self).setUp()

        self._stripe_original_attributes = {}

        for attr in self.RESTORE_ATTRIBUTES:
            self._stripe_original_attributes[attr] = getattr(stripe, attr)

        api_base = os.environ.get('STRIPE_API_BASE')
        if api_base:
            stripe.api_base = api_base
        stripe.api_key = os.environ.get(
            'STRIPE_API_KEY', 'tGN0bIwXnHdwOa85VABjPdSn8nWY7G7I')

        self.request_patchers = {}
        self.request_mocks = {}
        for lib in self.REQUEST_LIBRARIES:
            patcher = mock.patch("stripe.http_client.%s" % (lib,))

            self.request_mocks[lib] = patcher.start()
            self.request_patchers[lib] = patcher

        self.requestor_patcher = mock.patch(
            'stripe.api_requestor.APIRequestor')
        requestor_class_mock = self.requestor_patcher.start()
        self.requestor_mock = requestor_class_mock.return_value

        self.mock_response()

    def tearDown(self):
        super(StripeTestCaseMixin, self).tearDown()

        for attr in self.RESTORE_ATTRIBUTES:
            setattr(stripe, attr, self._stripe_original_attributes[attr])

        for patcher in self.request_patchers.itervalues():
            patcher.stop()

        self.requestor_patcher.stop()

    def mock_response(self, res={}):
        # self.requestor_mock.request = mock.Mock(return_value=(res, 'reskey'))

        mock_request = mock.Mock(return_value=(res, 'reskey'))

        def side_effect(method, url, params=None, headers=None):
            res = FakeStripeResponse(method, url).get_response()
            return (res, 'reskey')

        mock_request.side_effect = side_effect

        self.requestor_mock.request = mock_request


class SubscriptionTestMixin(object):

    def add_subscription(self, company):
        """
        add a (test) subscription for company
        """
        n = now()
        customer = company.get_customer()

        try:
            customer.current_subscription.delete()
        except CurrentSubscription.DoesNotExist:
            pass

        CurrentSubscription.objects.get_or_create(
            customer=customer,
            status=CurrentSubscription.STATUS_ACTIVE,
            plan='test',
            start=n,
            quantity=1,
            current_period_start=n,
            current_period_end=n + timedelta(days=1),
            amount=0
        )
