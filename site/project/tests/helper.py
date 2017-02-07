
import collections
import logging
import re
import time

from django.utils.timezone import now

from model_mommy import random_gen


# https://stackoverflow.com/questions/899067
# /how-should-i-verify-a-log-message-when-testing-python-code-under-nose
class TestLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict, in order,
    indexed by a lowercase log level string (e.g., 'debug', 'info', etc.).
    """

    def __init__(self, *args, **kwargs):
        self.messages = {
            'debug': collections.deque(),
            'info': collections.deque(),
            'warning': collections.deque(),
            'error': collections.deque(),
            'critical': collections.deque()
        }
        super(TestLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        "Store a message from ``record`` in the instance's ``messages`` dict."
        self.acquire()
        try:
            self.messages[record.levelname.lower()].append(record.getMessage())
        finally:
            self.release()

    def reset(self):
        self.acquire()
        try:
            for message_list in self.messages.values():
                message_list.clear()
        finally:
            self.release()


class FakeStripeResponser(object):
    """
    handle (fake) stripe responses
    """

    def __init__(self, method, url):
        self.method = method
        self.url = url

    def get_endpoint(self):
        """
        return api endpoint from url

        e.g. customer from /v1/customers/
        """
        regex = r'^/v\d+/(?P<endpoint>\w+)/?.*'
        match = re.match(regex, self.url)
        if match:
            return match.groupdict().get('endpoint', None)

    def get_response(self):
        """
        get (endpoint specific) response data or empty dict
        """
        endpoint = self.get_endpoint()
        if endpoint and hasattr(self, 'get_{}_response'.format(endpoint)):
            return getattr(self, 'get_{}_response'.format(endpoint))()
        return {}

    def get_customers_response(self):
        """
        return data for customers
        """
        customer_id = 'cus_{}'.format(random_gen.gen_uuid().hex[-14:])
        return {
            'id': customer_id,
            'object': 'customer',
            'account_balance': 0,
            "created": time.mktime(now().timetuple()),
            "currency": "chf",
            "default_source": None,
            "delinquent": False,
            "description": None,
            "discount": None,
            "email": "test@example.com",
            "livemode": False,
            "metadata": {},
            "shipping": None,
            "sources": {
                "object": "list",
                "data": [],
                "has_more": False,
                "total_count": 0,
                "url": "/v1/customers/{}/sources".format(customer_id)
            },
            "subscriptions": {
                "object": "list",
                "data": [],
                "has_more": False,
                "total_count": 0,
                "url": "/v1/customers/{}/subscriptions".format(customer_id)
            }
        }
