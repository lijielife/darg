
from django.conf import settings


def tracking(request):
    """get tracking enabled and tracking code and provide request"""
    tracking_enabled = getattr(
        settings, "TRACKING_ENABLED", not settings.DEBUG)
    tracking_id = getattr(settings, "TRACKING_CODE", None)
    debug = getattr(settings, "DEBUG", False)
    version = getattr(settings, "VERSION", False)
    dsn = getattr(settings, "RAVEN_CONFIG", False)
    res = dict(
        TRACKING_ENABLED=tracking_enabled,
        TRACKING_CODE=tracking_id,
        DEBUG=debug,
        request=request,
        VERSION=version,
        DSN=dsn['dsn_public']
    )
    return res


def default_protocol(request):
    return dict(protocol=settings.DEFAULT_HTTP_PROTOCOL)
