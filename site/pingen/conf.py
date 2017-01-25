
from __future__ import unicode_literals

from django.conf import settings
from django.test.signals import setting_changed


DEFAULTS = {
    # api urls
    'API_LIVE_URL': 'https://api.pingen.com',
    'API_TEST_URL': 'https://stage-api.pingen.com/',
    'API_TIMEOUT': None,

    # documents
    # Defines if a document is merely uploaded or also sent
    'SEND_ON_UPLOAD': False,  # default: False
    # Defines the sending speed if the document is automatically sent
    'SEND_SPEED': 2,  # 1 = priority, 2 = economy
    # Type of print
    'SEND_COLOR': 0,  # 0 = b/w (default), 1 = color, 2 = mixed
    # Paper handling
    'SEND_DUPLEX': 0,  # 0 = simplex (default), 1 = duplex
    # Address, If not passed, account default is taken.
    'RIGHT_ADDRESS': 0,  # 0 = address left, 1 = address right
    # Envelope ID of prepared and designed envelope in your account.
    'SEND_ENVELOPE': 0

}


class PingenSettings(object):
    """
    load settings from either global config or defaults

    For example:

        from pingen.conf import pingen_settings
        print(pingen_settings.SEND_ON_UPLOAD)

    """

    def __init__(self, user_settings=None, defaults=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'PINGEN', {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid pingen setting: '%s'" % attr)

        val = self.user_settings.get(attr)
        if not val:
            # try to fetch from global settings
            val = getattr(settings, 'PINGEN_{}'.format(attr), None)
        if not val:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


pingen_settings = PingenSettings()


# NOTE: just for tests
def reload_pingen_settings(*args, **kwargs):  # pragma: no cover
    global pingen_settings
    setting, value = kwargs['setting'], kwargs['value']
    if setting == 'PINGEN':
        pingen_settings = PingenSettings(value)


setting_changed.connect(reload_pingen_settings)
