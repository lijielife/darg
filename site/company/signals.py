
from django.contrib.flatpages.models import FlatPage
from django.core.cache import cache
from django.db.models.signals import post_save as post_save_signal


def _post_save_handler(sender, **kwargs):
    """
    clear flatpage urls cache
    """
    cache_key = 'company.middleware.CompanySubscriptionRequired.flatpage_urls'
    cache.delete(cache_key)


post_save_signal.connect(_post_save_handler, sender=FlatPage)
