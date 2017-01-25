
import json
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings

import mock
import requests

from model_mommy import random_gen

from project.tests.mixins import FakeResponseMixin

from ..api import Pingen as PingenAPI, APICall


class PingenTestCase(FakeResponseMixin, TestCase):

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

    @mock.patch.object(requests, 'post')
    def test_upload_document(self, mock_post):

        with self.assertRaises(ValueError):
            self.api.upload_document(None)

        with self.assertRaises(ValueError):
            self.api.upload_document('')

        doc = os.path.join(os.path.dirname(__file__), 'files', 'example.pdf')

        self.fake_response_content = json.dumps(dict())
        mock_post.return_value = self.get_fake_response('post')

        self.assertEqual(APICall.objects.count(), 0)

        self.assertFalse(self.api.upload_document(doc))

        self.assertEqual(APICall.objects.count(), 1)

        self.fake_response_content = json.dumps(dict(error=False))
        mock_post.return_value = self.get_fake_response('post')
        self.assertFalse(self.api.upload_document(doc))

        self.assertEqual(APICall.objects.count(), 2)

        self.fake_response_content = json.dumps(dict(error=False, id=1))
        mock_post.return_value = self.get_fake_response('post')
        self.assertTrue(self.api.upload_document(doc))

        self.assertEqual(APICall.objects.count(), 3)

        mock_post.return_value = self.get_fake_response(
            'post', status_code=400)
        self.assertFalse(self.api.upload_document(doc))

        self.assertEqual(APICall.objects.count(), 4)
