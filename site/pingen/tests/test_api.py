
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

# import mock
# import requests

from model_mommy import random_gen

from ..api import Pingen as PingenAPI


class PingenTestCase(TestCase):

    def setUp(self):
        self.api = PingenAPI(random_gen.gen_string(32))

    def test_init(self):
        token = random_gen.gen_string(32)
        api = PingenAPI(token)
        self.assertEqual(api.token, token)

        token = random_gen.gen_string(32)
        with override_settings(PINGEN_API_TOKEN=token):
            api = PingenAPI()
            self.assertEqual(api.token, token)

        with override_settings(PINGEN_API_TOKEN=None):
            with self.assertRaises(ImproperlyConfigured):
                PingenAPI()

    def test_get_api_url(self):
        path = random_gen.gen_string(20)

        url = self.api.get_api_url(path, include_token=False)
        self.assertTrue(url.startswith(settings.PINGEN_API_URL))
        self.assertTrue(url.endswith(path + '/'))

        url = self.api.get_api_url(path)
        self.assertTrue(url.endswith(path + '/token/' + self.api.token + '/'))

    # @mock.patch.object(requests, 'request')
    def test_upload_document(self, mock_request):
        # TODO
        pass
