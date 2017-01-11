#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from project.generators import (OperatorGenerator, OptionTransactionGenerator,
                                PositionGenerator, ShareholderGenerator)


class BaseViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.shareholder1 = ShareholderGenerator().generate()
        self.company = self.shareholder1.company
        self.operator = OperatorGenerator().generate(company=self.company)
        self.shareholder2 = ShareholderGenerator().generate()
        self.position1 = PositionGenerator().generate(buyer=self.shareholder1)
        self.position2 = PositionGenerator().generate(buyer=self.shareholder2)
        self.optiontransaction1 = OptionTransactionGenerator().generate(
            buyer=self.shareholder1)
        self.optiontransaction2 = OptionTransactionGenerator().generate(
            buyer=self.shareholder2)


class ShareholderViewTestCase(BaseViewTestCase):

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


class PositionViewTestCase(BaseViewTestCase):

    def test_view(self):
        """
        test shareholder detail view
        """
        self.client.force_login(self.operator.user)

        res = self.client.get(reverse('position',
                              kwargs={'pk': self.position1.pk}))
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse('position',
                              kwargs={'pk': self.position2.pk}))
        self.assertEqual(res.status_code, 302)  # redirect to login
        self.assertIn('login', res.url)


class OptionTransactionViewTestCase(BaseViewTestCase):

    def test_view(self):
        """
        test shareholder detail view
        """
        self.client.force_login(self.operator.user)

        res = self.client.get(reverse('optiontransaction',
                              kwargs={'pk': self.optiontransaction1.pk}))
        self.assertEqual(res.status_code, 200)

        res = self.client.get(reverse('optiontransaction',
                              kwargs={'pk': self.optiontransaction2.pk}))
        self.assertEqual(res.status_code, 302)  # redirect to login
        self.assertIn('login', res.url)
