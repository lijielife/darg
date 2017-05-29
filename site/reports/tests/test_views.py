#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.core import mail
from django.core.urlresolvers import reverse
from django.test import Client, TestCase
from django.utils import timezone
# from model_mommy import mommy

from project.generators import (DEFAULT_TEST_DATA, CompanyGenerator,
                                ComplexOptionTransactionsGenerator,
                                ComplexShareholderConstellationGenerator,
                                OperatorGenerator, PositionGenerator,
                                ReportGenerator, SecurityGenerator,
                                ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator)
from project.tests.mixins import (MoreAssertsTestCaseMixin,
                                  SubscriptionTestMixin)
from reports.views import _get_contacts, _get_transactions
from shareholder.models import Company, OptionTransaction
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

    def test_printed_certificates_xls(self):
        """
        download of all certificates which are printed
        """
        now = timezone.now()
        positions, shs = ComplexOptionTransactionsGenerator().generate()  # noqa
        OptionTransaction.objects.filter(
            pk__in=[ot.pk for ot in positions]).update(printed_at=now)
        other_operator = OperatorGenerator().generate()
        operator = shs[0].company.operator_set.first()
        company = operator.company
        self.add_subscription(company)
        pos = PositionGenerator().generate(company=company)
        pos.printed_at = timezone.now()
        pos.certificate_id = '88888'
        pos.save()

        # run test for unauth'd user
        url = reverse('reports:printed_certificates_xls',
                      kwargs={"company_id": company.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        # foreign operator must not access data
        is_loggedin = self.client.login(username=other_operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # company operator can access data
        is_loggedin = self.client.login(username=operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        with self.assertLessNumQueries(44):
            response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contacts_xls(self):
        """ test download of all shareholders contact data """
        # run test
        response = self.client.get(
            reverse('reports:contacts_xls',
                    kwargs={"company_id": self.company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        self.client.force_login(user)

        response = self.client.get(
            reverse('reports:contacts_xls',
                    kwargs={"company_id": self.company.id}))

        # assert response code
        self.assertEqual(response.status_code, 403)

    def test_get_contacts(self):
        """ get xls list array of contacts data """
        ComplexShareholderConstellationGenerator().generate()

        company = Company.objects.last()
        with self.assertLessNumQueries(46):
            res = _get_contacts(company)
        self.assertTrue(len(res) > 1)
        self.assertEqual(len(res[0]), 15)
        self.assertEqual(len(res[1]), 15)  # no nationality
        self.assertEqual(res[0][0].encode('utf8'), u'0')

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

    def test_vested_xls(self):
        """
        download of all shares and options which are vested
        """
        positions, shs = ComplexOptionTransactionsGenerator().generate()  # noqa
        OptionTransaction.objects.filter(
            pk__in=[ot.pk for ot in positions]).update(vesting_months=24)
        other_operator = OperatorGenerator().generate()
        operator = shs[0].company.operator_set.first()
        company = operator.company
        self.add_subscription(company)
        shs2, s1 = ComplexShareholderConstellationGenerator().generate(
            company=company, shareholder_count=10)
        for s in shs2:
            s.buyer.all().update(vesting_months=12)

        # run test for unauth'd user
        response = self.client.get(
            reverse('reports:vested_xls',
                    kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 302)

        # foreign operator must not access data
        is_loggedin = self.client.login(username=other_operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(
            reverse('reports:vested_xls',
                    kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 302)
        self.client.logout()

        # company operator can access data
        is_loggedin = self.client.login(username=operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        with self.assertLessNumQueries(96):
            response = self.client.get(
                reverse('reports:vested_xls',
                        kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 200)
