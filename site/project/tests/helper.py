
import re
import time

from django.utils.timezone import now

from model_mommy import random_gen


class FakeStripeResponse(object):
    """
    handle (fake) stripe responses
    """

    def __init__(self, method, url):
        self.method = method
        self.url = url

    def get_endpoint(self):
        """
        return api endpoint from url

        e.g. customer from /v1/customer/
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
                "data": [

                ],
                "has_more": False,
                "total_count": 0,
                "url": "/v1/customers/{}/subscriptions".format(customer_id)
            }
        }
