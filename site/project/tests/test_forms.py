#!/usr/bin/python
# -*- coding: utf-8 -*-
from model_mommy import mommy
from django.conf import settings
from django.test import TestCase

from project.forms import RegistrationForm


class RegistrationFormTestCase(TestCase):

    def setUp(self):
        user = mommy.prepare(settings.AUTH_USER_MODEL, _fill_optional=True)
        self.form = RegistrationForm({
            'username': user.username,
            'email': user.email,
            'tos': True,
            'password1': 'asdf',
            'password2': 'asdf',
        })

    def test_form(self):
        """
        tos field is there and has changed text with link
        """
        self.assertIn('tos', self.form.fields.keys())
        self.assertIn('link tos', self.form.fields.get('tos').label)
        self.assertIn('agb', self.form.fields.get('tos').label)

    def test_save(self):
        user = self.form.save()
        self.assertIsNotNone(user.auth_token)
        self.assertIsNotNone(user.userprofile)
        self.assertTrue(user.userprofile.tnc_accepted)
