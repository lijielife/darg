
from django.test import TestCase

from model_mommy import random_gen

from ..mail import is_valid_email


class MailUtilsTestCase(TestCase):

    def test_is_valid_email(self):
        self.assertFalse(is_valid_email(random_gen.gen_string(10)))
        self.assertTrue(is_valid_email(random_gen.gen_email()))
