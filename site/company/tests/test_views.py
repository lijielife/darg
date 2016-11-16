#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _

from project.generators import (
    CompanyGenerator, SecurityGenerator,
    OperatorGenerator, DEFAULT_TEST_DATA, UserGenerator)


class CompanyAdminDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = CompanyGenerator().generate()
        self.user = UserGenerator().generate()

    def test_view(self):

        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        self.client.force_login(self.user)
        res = self.client.get(reverse('admin:shareholder_company_change',
                                      args=[self.company.pk]))

        self.assertEqual(res.status_code, 200)


class CompanyDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_numbered_shares(self):

        company = CompanyGenerator().generate()
        SecurityGenerator().generate(
            company=company, track_numbers=True)
        operator = OperatorGenerator().generate(company=company)

        self.client.login(username=operator.user.username,
                          password=DEFAULT_TEST_DATA.get('password'))

        res = self.client.get(reverse(
            'company', kwargs={'company_id': company.id}))

        self.assertEqual(res.status_code, 200)
        self.assertIn(
            _('tracking security numbers for owners enabled. segments:'),
            res.content)
