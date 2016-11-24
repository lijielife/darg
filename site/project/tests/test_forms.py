#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase

from project.forms import RegistrationForm


class RegistrationFormTestCase(TestCase):

    def setUp(self):
        self.form = RegistrationForm()

    def test_form(self):
        """
        tos field is there and has changed text with link
        """
        self.assertIn('tos', self.form.fields.keys())
        self.assertIn('link tos', self.form.fields.get('tos').label)
        self.assertIn('agb', self.form.fields.get('tos').label)
