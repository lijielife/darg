
from django.test import TestCase

from ..conf import PingenSettings, DEFAULTS


class PingenSettingsTestCase(TestCase):

    def test_init(self):
        settings = PingenSettings()
        self.assertEqual(settings.SEND_SPEED, DEFAULTS.get('SEND_SPEED'))

        user_settings = dict(SEND_SPEED=1)
        settings = PingenSettings(user_settings=user_settings)
        self.assertNotEqual(settings.SEND_SPEED, DEFAULTS.get('SEND_SPEED'))
        self.assertEqual(settings.SEND_SPEED, user_settings.get('SEND_SPEED'))
