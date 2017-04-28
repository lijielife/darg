#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from project.generators import (OperatorGenerator, ReportGenerator,
                                UserGenerator)
from project.tests.mixins import SubscriptionTestMixin
from utils.http import get_file_content_as_string
from utils.session import add_company_to_session


class BaseReportViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.report = ReportGenerator().generate()
        self.report.render()
        self.operator = OperatorGenerator().generate(
            user=self.report.user, company=self.report.company)
        self.other_user = UserGenerator().generate()


class IndexViewTestCase(SubscriptionTestMixin, BaseReportViewTestCase):

    def test_display(self):
        """ confirm reports index page content """
        self.add_subscription(self.report.company)
        response = self.client.get(reverse('reports:reports'))
        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.operator.user)
        response = self.client.get(reverse('reports:reports'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(reverse('statement_reports'),
                      response.content.decode('utf-8'))


class ReportDownloadTestCase(SubscriptionTestMixin, BaseReportViewTestCase):

    def test_report_download(self):
        """ secure download of file attached to report """
        # perm check: unauth'd
        response = self.client.get(
            reverse('reports:download', kwargs={'report_id': self.report.pk}))
        self.assertEqual(response.status_code, 302)

        # perm check: other user
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse('reports:download', kwargs={'report_id': self.report.pk}))
        self.assertEqual(response.status_code, 403)

        # perm check: proper user
        self.client.force_login(self.report.user)
        add_company_to_session(self.client.session, self.report.company)
        self.add_subscription(self.report.company)
        response = self.client.get(
            reverse('reports:download', kwargs={'report_id': self.report.pk}))
        self.assertEqual(response.status_code, 200)

        # content check
        content = get_file_content_as_string(response)
        self.assertIn('PDF', content)
