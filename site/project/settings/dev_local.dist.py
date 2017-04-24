DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'darg',
        'USER': 'darg',
        'PASSWORD': 'darg',
        'HOST': 'localhost'
    }
}
SITE_ID = 3
SECRET_KEY = 't@0=8$(m3+gcpf#a+z2&$=q+po--_&5n4#c8o%!s-5h$w)x2m3'

# --- SUBSCRIPTION
import inspect

CREATE_STRIPE_CUSTOMER_FOR_SUBSCRIBER_ON_CREATE = False

ALL_FEATURES = {}
SUBSCRIPTION_FEATURES = inspect.currentframe().f_back.f_globals.get(
    'SUBSCRIPTION_FEATURES', {})
[ALL_FEATURES.update(
    # NOTE: we only have create validators for now
    {feature: {'validators': {'create': []}}})
    for feature in SUBSCRIPTION_FEATURES.keys()]

DJSTRIPE_PLANS = {
    'test': {
        'stripe_plan_id': 'test',
        'name': 'Test Plan',
        'price': 0,
        'currency': 'chf',
        'interval': 'day',
        'features': ALL_FEATURES,
        'validators': []
    }
}
