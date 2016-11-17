#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from project.generators import ShareholderGenerator, OperatorGenerator


class ShareholderViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.shareholder1 = ShareholderGenerator().generate()
        self.company = self.shareholder1.company
        self.operator = OperatorGenerator().generate(company=self.company)
        self.shareholder2 = ShareholderGenerator().generate()

    def test_view(self):
        """
        test shareholder detail view
        """
        self.client.force_login(self.operator.user)

        res = self.client.get(reverse('shareholder',
                              kwargs={'pk': self.shareholder1.pk}))
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse('shareholder',
                              kwargs={'pk': self.shareholder2.pk}))
        self.assertEqual(res.status_code, 302)  # redirect to login
        self.assertIn('login', res.url)
