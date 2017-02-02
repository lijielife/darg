#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase, Client, modify_settings
from django.core.urlresolvers import reverse
from django.utils.translation import gettext as _

import mock

from two_factor.admin import AdminSiteOTPRequiredMixin

from project.generators import (
    CompanyGenerator, SecurityGenerator,
    OperatorGenerator, DEFAULT_TEST_DATA, UserGenerator)


class CompanyAdminDetailViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.company = CompanyGenerator().generate()
        self.user = UserGenerator().generate()

    # disable two-factor authentication
    @modify_settings(MIDDLEWARE_CLASSES={
        'remove': ['django_otp.middleware.OTPMiddleware']
    })
    @mock.patch.object(AdminSiteOTPRequiredMixin, 'has_permission',
                       return_value=True)
    def test_view(self, mock_permission):

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
