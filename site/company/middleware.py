
import re

from django.shortcuts import redirect, resolve_url
# django 1.10
# from django.utils.deprecation import MiddlewareMixin

from utils.session import get_company_from_request


# class CompanySubscriptionRequired(MiddlewareMixin):
class CompanySubscriptionRequired(object):
    """
    middleware to make sure a company has an active subscription
    """

    BLACKLIST_URLS = [
        r'^positions/',
        r'^options/',
        r'^shareholder/',
        r'^optionsplan/',
        r'^reports/',
    ]

    def process_request(self, request):

        path = request.path.lstrip('/')

        if (request.user.is_authenticated() and
                any(re.compile(m).match(path) for m in self.BLACKLIST_URLS)):
            # check if any companies have no active subscription
            company = get_company_from_request(request, fail_silently=True)
            if company:
                customer = company.get_customer()
                if customer and not customer.has_active_subscription():
                    redirect_url = resolve_url(
                        'djstripe:subscribe',
                        **dict(company_id=company.pk)
                    )
                    return redirect(redirect_url)
