
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
