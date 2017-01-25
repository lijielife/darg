
from django.contrib import admin
from django.test import TestCase

from model_mommy import mommy, random_gen

from ..admin import APICall, APICallAdmin


class APICallAdminTestCase(TestCase):

    def setUp(self):
        self.admin = APICallAdmin(APICall, admin.site)
        self.instance = mommy.prepare(APICall)

    def test_url(self):
        valid_string = random_gen.gen_string(50)
        self.instance.url = valid_string
        self.assertEqual(valid_string, self.admin._url(self.instance))

        invalid_string = random_gen.gen_string(120)
        self.instance.url = invalid_string
        self.assertNotEqual(invalid_string, self.admin._url(self.instance))
        self.assertTrue(len(self.admin._url(self.instance)) == 100)
        self.assertTrue(self.admin._url(self.instance).endswith('...'))
