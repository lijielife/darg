#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import datetime
import StringIO

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils.translation import ugettext as _
from rest_framework.test import APIClient

from project.generators import (DEFAULT_TEST_DATA, CompanyGenerator,
                                ComplexOptionTransactionsGenerator,
                                ComplexShareholderConstellationGenerator,
                                OperatorGenerator, PositionGenerator,
                                SecurityGenerator, ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator,
                                OptionTransactionGenerator, ReportGenerator)
from project.tests.mixins import MoreAssertsTestCaseMixin
from project.views import _get_contacts, _get_transactions
from shareholder.models import (Company, OptionTransaction, Security,
                                Shareholder, UserProfile)
from utils.http import get_file_content_as_string


def _add_company_to_user_via_rest(user):

    client = APIClient()
    response = client.post(
        '/services/rest/api-token-auth/',
        {'username': user.username, 'password': 'test'},
        format='json'
    )
    token = user.auth_token

    response = client.post(
        reverse('add_company'), {
            'name': 'company',
            'founded_at': '2015-01-02T23:00:00.000Z',
            'share_count': 1,
            'face_value': 2
        },
        **{
            'HTTP_AUTHORIZATION': 'Token {}'.format(token.key),
            'format': 'json',
        }
    )

    if response.status_code in [200, 201]:
        return True

    return False


class IndexTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = UserGenerator().generate()

    def test_index_content(self):

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(u'Login', response.content.decode('utf8'))
        self.assertTrue("last css in" in response.content)

    def test_index_content_authd(self):
        """
        index page for logged in user
        """

        self.client.force_login(self.user)
        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(_('My Dashboard'), response.content.decode('utf8'))


class InstapageTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        """
        user arriving from instapage must be imported, logged in and redirected
        """

        if not settings.INSTPAGE_ENABLED:
            return

        response = self.client.get(reverse('instapage'), follow=True)

        self.assertEqual(response.status_code, 400)

        response = self.client.get(
            reverse('instapage') + '?submission=30122798', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            User.objects.filter(
                email='jirka@tschitschereengreen.com',
                first_name='Jirka',
                last_name='Schaefer',
                is_active=True
                ).exists())
        self.assertIn('_auth_user_id', self.client.session)
        self.assertEqual(
            response.redirect_chain[0][0], '/start/')
        self.assertTrue(UserProfile.objects.filter(
            user__email='jirka@tschitschereengreen.com',
            tnc_accepted=True, ip='79.168.182.174').exists())
        # FIXME
        # self.assertEqual(len(mail.outbox), 1)

    def test_get_existing(self):
        """
        user arriving from instapage must be imported, logged in and redirected
        """

        if not settings.INSTPAGE_ENABLED:
            return

        response = self.client.get(reverse('instapage'), follow=True)

        self.assertEqual(response.status_code, 400)

        # call twice
        response = self.client.get(
            reverse('instapage') + '?submission=30122798', follow=True)
        response = self.client.get(
            reverse('instapage') + '?submission=30122798', follow=True)

        msg = _(u'You have already an existing user account. '
                'Please login or reset your password.')
        self.assertRedirects(response, reverse('two_factor:login'))
        self.assertContains(response, msg)


class TrackingTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_tracking_for_debug_mode(self):

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)

    def test_start_authorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(
            username=user.username, password=DEFAULT_TEST_DATA['password'])

        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)
        self.assertTrue("Willkommen" in response.content)
        self.assertTrue("shareholder_list" in response.content)
        # self.assertTrue('download/pdf' in response.content)
        # self.assertTrue('download/csv' in response.content)

    def test_start_authorized_with_operator(self):

        user = UserGenerator().generate()

        is_operator_added = _add_company_to_user_via_rest(user)
        self.assertTrue(is_operator_added)

        is_loggedin = self.client.login(
            username=user.username, password=DEFAULT_TEST_DATA['password'])

        self.assertTrue(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("UA-58468401-4" in response.content)
        self.assertTrue("Willkommen" in response.content)
        self.assertTrue("shareholder_list" in response.content)

    def test_start_nonauthorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(
            username=user.username, password='invalid_pw')
        self.assertFalse(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)
        self.assertEqual(response.status_code, 200)
        # redirect to login
        self.assertIn(_('Register'), response.content.decode('utf-8'))


class DownloadTestCase(MoreAssertsTestCaseMixin, TestCase):

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

    def test_captable_csv_download(self):
        """ rest download of captable csv """

        # data
        company = CompanyGenerator().generate()
        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(
                company=company, number=str(x)))
        shareholder_list = sorted(
            shareholder_list, key=lambda t: t.user.last_name.lower())

        # initial share creation
        PositionGenerator().generate(
            seller=None,
            buyer=shareholder_list[0], count=1000, value=10)
        # single transaction
        PositionGenerator().generate(
            buyer=shareholder_list[1], count=10, value=10,
            seller=shareholder_list[0])
        # shareholder bought and sold
        PositionGenerator().generate(
            buyer=shareholder_list[2], count=20, value=20,
            seller=shareholder_list[0])
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=20, value=20,
            seller=shareholder_list[2])

        # login and retest
        report = ReportGenerator().generate(company=company, file_type='CSV')
        report.render()
        user = report.user
        OperatorGenerator().generate(user=user, company=company)
        self.client.force_login(user)
        response = self.client.get(reverse('reports:download',
                                   kwargs={"report_id": report.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)

        # assert proper csv
        content = get_file_content_as_string(response)
        fileobj = StringIO.StringIO(content)
        reader = csv.reader(fileobj, delimiter=',')
        lines = list(reader)
        for row in lines:
            self.assertEqual(len(row), 28)
        self.assertEqual(len(lines), 6)  # ensure we have the right data
        # assert company itself
        self.assertIn(shareholder_list[0].number,
                      [f[0] for f in lines])
        # assert share owner
        self.assertIn(shareholder_list[1].number,
                      [f[0] for f in lines])
        # assert shareholder witout position not in there
        for line in lines:
            self.assertNotEqual(line[0], shareholder_list[3].number)
        # assert shareholder which bought and sold again
        for line in lines:
            self.assertNotEqual(line[0], shareholder_list[2].number)

    def test_csv_download_number_segments(self):
        """ rest download of captable csv """

        # data
        company = CompanyGenerator().generate()
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
        report = ReportGenerator().generate(company=company, file_type='CSV')
        report.render()
        user = report.user
        OperatorGenerator().generate(user=user, company=company)
        self.client.force_login(user)
        response = self.client.get(reverse('reports:download',
                                   kwargs={"report_id": report.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        content = get_file_content_as_string(response)
        lines = content.split('\r\n')
        lines.pop()  # remove last element based on final '\r\n'
        for row in lines:
            if row == lines[0]:  # skip first row
                continue
            self.assertEqual(row.count(','), 31)
            fields = row.split(',')
            s = Shareholder.objects.get(company=company, number=fields[0])
            text = s.current_segments(security)
            if text:
                self.assertTrue(text in fields[8])
            self.assertIn(_('None'), fields[31])

    def test_pdf_download_with_number_segments(self):
        """ test download of captable pdf """
        company = CompanyGenerator().generate()
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
        # assert proper csv
        content = get_file_content_as_string(response)
        self.assertTrue(content.startswith('%PDF'))

    def test_printed_certificates_csv(self):
        """
        download of all certificates which are printed
        """
        now = datetime.datetime.now()
        positions, shs = ComplexOptionTransactionsGenerator().generate()  # noqa
        OptionTransaction.objects.filter(
            pk__in=[ot.pk for ot in positions]).update(printed_at=now)
        other_operator = OperatorGenerator().generate()
        operator = shs[0].company.operator_set.first()
        company = operator.company
        pos = PositionGenerator().generate(company=company)
        pos.printed_at = datetime.datetime.now()
        pos.certificate_id = '88888'
        pos.save()

        # run test for unauth'd user
        response = self.client.get(
            reverse('printed_certificates_csv',
                    kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 302)

        # foreign operator must not access data
        is_loggedin = self.client.login(username=other_operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(
            reverse('printed_certificates_csv',
                    kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # company operator can access data
        is_loggedin = self.client.login(username=operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        with self.assertLessNumQueries(41):
            response = self.client.get(
                reverse('printed_certificates_csv',
                        kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 200)

        # assert proper csv
        content = response.content
        lines = content.split('\r\n')
        lines.pop()  # remove last element based on final '\r\n'
        for row in lines[1:]:
            self.assertEqual(row.count(','), 5)
        self.assertEqual(len(lines), 8)  # ensure we have the right data
        # assert company itself
        self.assertIn(shs[0].get_full_name(), [f.split(',')[0] for f in lines])
        # assert share owner
        self.assertIn(shs[1].get_full_name(), [f.split(',')[0] for f in lines])

    def test_contacts_csv(self):
        """ test download of all shareholders contact data """
        company = CompanyGenerator().generate()
        # run test
        response = self.client.get(
            reverse('contacts_csv', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        self.client.force_login(user)

        response = self.client.get(
            reverse('contacts_csv', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 403)

    def test_get_contacts(self):
        """ get csv list array of contacts data """
        ComplexShareholderConstellationGenerator().generate()

        company = Company.objects.last()
        with self.assertLessNumQueries(44):
            res = _get_contacts(company)
        self.assertTrue(len(res) > 1)
        self.assertEqual(len(res[0]), 15)
        self.assertEqual(len(res[1]), 15)  # no nationality
        self.assertEqual(res[0][0], _(u'shareholder number'))

    def test_transactions_csv(self):
        """ test download of all transactions data
        /company/3/download/transactions?from=2017-01-12T23:00:00.000Z&to=2017-01-13T23:00:00.000Z&security=56
        """
        company = CompanyGenerator().generate()
        security = SecurityGenerator().generate(company=company)
        # run test
        response = self.client.get(
            reverse('transactions_csv', kwargs={"company_id": company.id}),
            {'to': '2017-01-12T23:00:00.000Z',
             'from': '2011-01-12T23:00:00.000Z',
             'security': security.pk})

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        self.client.force_login(user)

        response = self.client.get(
            reverse('transactions_csv', kwargs={"company_id": company.id}),
            {'to': '2017-01-12T23:00:00.000Z',
             'from': '2011-01-12T23:00:00.000Z',
             'security': security.pk})

        # assert response code
        self.assertEqual(response.status_code, 403)

    def test_get_transactions(self):
        """ get csv list array of contacts data """
        ComplexShareholderConstellationGenerator().generate()

        company = Company.objects.last()
        from_date = datetime.datetime(2013, 1, 1)
        to_date = datetime.datetime(2099, 1, 1)
        with self.assertLessNumQueries(38):
            res = _get_transactions(
                from_date, to_date, Security.objects.filter(
                    company=company).first(), company)
        self.assertTrue(len(res) > 1)
        self.assertEqual(len(res[0]), 11)
        self.assertEqual(len(res[1]), 9)  # no nationality
        self.assertEqual(res[0][0], _(u'date'))

    def test_vested_csv(self):
        """
        download of all shares and options which are vested
        """
        positions, shs = ComplexOptionTransactionsGenerator().generate()  # noqa
        OptionTransaction.objects.filter(
            pk__in=[ot.pk for ot in positions]).update(vesting_months=24)
        other_operator = OperatorGenerator().generate()
        operator = shs[0].company.operator_set.first()
        company = operator.company
        shs2, s1 = ComplexShareholderConstellationGenerator().generate(
            company=company, shareholder_count=10)
        for s in shs2:
            s.buyer.all().update(vesting_months=12)

        # run test for unauth'd user
        response = self.client.get(
            reverse('vested_csv',
                    kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 302)

        # foreign operator must not access data
        is_loggedin = self.client.login(username=other_operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(
            reverse('vested_csv',
                    kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        # company operator can access data
        is_loggedin = self.client.login(username=operator.user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        with self.assertLessNumQueries(93):
            response = self.client.get(
                reverse('vested_csv',
                        kwargs={"company_id": company.id}))
        self.assertEqual(response.status_code, 200)

        # assert proper csv
        content = response.content
        lines = content.split('\r\n')
        lines.pop()  # remove last element based on final '\r\n'
        for row in lines[1:]:
            self.assertEqual(row.count(','), 5)
        self.assertEqual(len(lines), 21)  # ensure we have the right data
        # assert company itself
        self.assertIn(shs[0].get_full_name(), [f.split(',')[0] for f in lines])
        # assert share owner
        self.assertIn(shs[1].get_full_name(), [f.split(',')[0] for f in lines])

    def test_option_pdf(self):
        """ test printable certificate """
        ot = OptionTransactionGenerator().generate()
        company = ot.option_plan.company
        # run test
        response = self.client.get(
            reverse('option_pdf', kwargs={"option_id": ot.pk}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        with self.assertLessNumQueries(53):
            response = self.client.get(
                reverse('option_pdf', kwargs={"option_id": ot.pk}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        content = response.content
        self.assertTrue(content.startswith('%PDF'))
        self.assertTrue(content.endswith('EOF\n'))

    def test_position_option_pdf(self):
        """ test printable certificate """
        pos = PositionGenerator().generate()
        company = pos.buyer.company
        # run test
        response = self.client.get(
            reverse('position_option_pdf', kwargs={"option_id": pos.pk}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        with self.assertLessNumQueries(55):
            response = self.client.get(
                reverse('position_option_pdf', kwargs={"option_id": pos.pk}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        content = response.content
        self.assertTrue(content.startswith('%PDF-1'))
        self.assertTrue(content.endswith('EOF\n'))
