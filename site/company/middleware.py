
import re

from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.cache import cache
from django.shortcuts import redirect, resolve_url


class CompanySubscriptionRequired(object):
    """
    middleware to make sure a company has an active subscription
    """

    BLACKLIST_URLS = [
        r'^positions/',
        r'^options/',
        r'^shareholder/',
        r'^optionsplan/'
    ]

    def process_request(self, request):

        path = request.path.lstrip('/')

        if (request.user.is_authenticated() and
                any(re.compile(m).match(path) for m in self.BLACKLIST_URLS)):
            # check if any companies have no active subscription
            for operator in request.user.operator_set.all():
                customer = operator.company.get_customer()
                if customer and not customer.has_active_subscription():
                    redirect_url = resolve_url(
                        'djstripe:subscribe',
                        **dict(company_id=operator.company_id)
                    )
                    return redirect(redirect_url)
