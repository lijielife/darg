#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.utils import timezone
# from model_mommy import mommy

from project.generators import (CompanyGenerator,
                                ComplexShareholderConstellationGenerator,
                                OperatorGenerator, PositionGenerator,
                                ReportGenerator, SecurityGenerator,
                                ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator)
from project.tests.mixins import (MoreAssertsTestCaseMixin,
                                  SubscriptionTestMixin)
from reports.views import _get_transactions
from shareholder.models import Company
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


class DownloadTestCase(MoreAssertsTestCaseMixin, SubscriptionTestMixin,
                       TestCase):

    def _get_attachment_content(self, idx=None):
        """ from email with idx inside mail.outbox, get the first attachments
        string content
        """
        msgs = [msg for msg in mail.outbox if msg.attachments]
        msg = msgs[idx or 0]
        attn = msg.attachments[0]
        return attn[0], attn[1]

    def setUp(self):
        self.client = Client()
        self.company = CompanyGenerator().generate()
        self.shs, self.s = ComplexShareholderConstellationGenerator().generate(
            company=self.company)

    def test_captable_xls_download(self):
        """ rest download of captable xls """

        # data
        company = CompanyGenerator().generate()
        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(
                company=company, number=str(x)))
        shareholder_list = sorted(
            shareholder_list, key=lambda t: t.user.last_name.lower())

        # initial share creation
        p = PositionGenerator().generate(
            seller=None,
            buyer=shareholder_list[0], count=1000, value=10)
        security = p.security
        # single transaction
        PositionGenerator().generate(
            buyer=shareholder_list[1], count=10, value=10,
            seller=shareholder_list[0], security=security)
        # shareholder bought and sold
        PositionGenerator().generate(
            buyer=shareholder_list[2], count=20, value=20,
            seller=shareholder_list[0], security=security)
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=20, value=20,
            seller=shareholder_list[2], security=security)

        # login and retest
        report = ReportGenerator().generate(company=company, file_type='XLS')
        report.render()
        user = report.user
        OperatorGenerator().generate(user=user, company=company)
        self.add_subscription(company)
        self.client.force_login(user)
        response = self.client.get(reverse('reports:download',
                                   kwargs={"report_id": report.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)

    def test_xls_download_number_segments(self):
        """ rest download of captable xls """

        # data
        company = CompanyGenerator().generate()
        self.add_subscription(company)
        secs = TwoInitialSecuritiesGenerator().generate(company=company)
        security = secs[1]
        security.track_numbers = True
        security.save()

        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(
                company=company, number=str(x)))

        # initial share creation
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=1000, value=10, security=security)
        # single transaction
        PositionGenerator().generate(
            buyer=shareholder_list[1], count=10, value=10, security=security,
            seller=shareholder_list[0])
        # shareholder bought and sold
        PositionGenerator().generate(
            buyer=shareholder_list[2], count=20, value=20, security=security,
            seller=shareholder_list[0])
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=20, value=20, security=security,
            seller=shareholder_list[2])

        # login and retest
        report = ReportGenerator().generate(company=company, file_type='XLS')
        report.render()
        user = report.user
        OperatorGenerator().generate(user=user, company=company)
        self.client.force_login(user)
        response = self.client.get(reverse('reports:download',
                                   kwargs={"report_id": report.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)

    def test_pdf_download_with_number_segments(self):
        """ test download of captable pdf """
        company = CompanyGenerator().generate()
        self.add_subscription(company)
        secs = TwoInitialSecuritiesGenerator().generate(company=company)
        report = ReportGenerator().generate(company=company)
        report.render()
        user = report.user
        OperatorGenerator().generate(user=user, company=company)
        security = secs[1]
        security.track_numbers = True
        security.save()

        self.client.force_login(user)
        response = self.client.get(reverse('reports:download',
                                           kwargs={"report_id": report.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper xls
        content = get_file_content_as_string(response)
        self.assertTrue(content.startswith('%PDF'))

    def test_transactions_xls(self):
        """ test download of all transactions data
        /company/3/download/transactions?from=2017-01-12T23:00:00.000Z&to=2017-01-13T23:00:00.000Z&security=56
        """
        company = CompanyGenerator().generate()
        security = SecurityGenerator().generate(company=company)
        # run test
        response = self.client.get(
            reverse('reports:transactions_xls',
                    kwargs={"company_id": company.id}),
            {'to': '2017-01-12T23:00:00.000Z',
             'from': '2011-01-12T23:00:00.000Z',
             'security': security.pk})

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        self.client.force_login(user)

        response = self.client.get(
            reverse('reports:transactions_xls',
                    kwargs={"company_id": company.id}),
            {'to': '2017-01-12T23:00:00.000Z',
             'from': '2011-01-12T23:00:00.000Z',
             'security': security.pk})

        # assert response code
        self.assertEqual(response.status_code, 403)

    def test_get_transactions(self):
        """ get xls list array of contacts data """
        shs, sec = ComplexShareholderConstellationGenerator().generate()

        company = Company.objects.last()
        from_date = timezone.make_aware(datetime.datetime(2013, 1, 1))
        to_date = timezone.make_aware(datetime.datetime(2099, 1, 1))
        with self.assertLessNumQueries(38):
            res = _get_transactions(
                from_date, to_date, sec, company)
        self.assertTrue(len(res) > 1)
        self.assertEqual(len(res[0]), 9)
