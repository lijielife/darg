
import re

from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.cache import cache
from django.shortcuts import redirect, resolve_url


class CompanySubscriptionRequired(object):
    """
    middleware to make sure a company has an active subscription
    """

    EXEMPT_URLS = [
        r'^admin/', r'^__adm/',
        # r'^start/$',
        r'^accounts/',
        r'^instapage/',
        r'^jsi18n/',
        r'^blog/',
        r'^comments/',
        r'^markdown/',
        r'^rosetta/',
        r'^sitemap',
        r'^_403/$',
        r'^_404/$',
        r'^_500/$',
        r'^markdownx/',
        r'^_stripe/webhooks/$',
        r'^{}'.format(settings.STATIC_URL),
        r'^{}'.format(settings.MEDIA_URL),
        r'^company/\d+/subscriptions/'
    ]

    def process_request(self, request):
        path = request.path.lstrip('/')

        exempt_urls = self.EXEMPT_URLS
        # add flatpage urls
        flatpage_urls = self._get_flatpage_urls()
        [exempt_urls.append(flatpage_url) for flatpage_url in flatpage_urls]

        if (request.user.is_authenticated() and
                not any(re.compile(m).match(path) for m in exempt_urls)):
            # check if any companies have no active subscription
            for operator in request.user.operator_set.all():
                customer = operator.company.get_customer()
                if customer and not customer.has_active_subscription():
                    redirect_url = resolve_url(
                        'djstripe:subscribe',
                        **dict(company_id=operator.company_id)
                    )
                    print('redirect', request.path)
                    return redirect(redirect_url)

    def _get_flatpage_urls(self):
        """
        get flatpage urls from cache (or set if not exists)
        """
        cache_key = (
            'company.middleware.CompanySubscriptionRequired.flatpage_urls')
        flatpage_urls = cache.get(cache_key)
        if not flatpage_urls:
            flatpages = FlatPage.objects.filter(sites=settings.SITE_ID)
            flatpage_urls = [flatpage.url for flatpage in flatpages]
            cache.set(cache_key, flatpage_urls)
        return flatpage_urls
