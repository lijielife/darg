#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils.translation import ugettext as _
from rest_framework.test import APIClient

from project.generators import (CompanyGenerator, OperatorGenerator,
                                PositionGenerator, ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator,
                                DEFAULT_TEST_DATA, SecurityGenerator,
                                ComplexShareholderConstellationGenerator)
from project.views import _get_contacts, _get_transactions
from shareholder.models import Shareholder, UserProfile, Company, Security


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
            'count': 1,
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
        self.assertTrue("bootstrap.min.js" in response.content)
        self.assertTrue("xeditable.min.js" in response.content)
        self.assertTrue("xeditable.css" in response.content)
        self.assertTrue("last css in" in response.content)
        self.assertIn(u'Login', response.content.decode('utf8'))

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

        try:

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

        except Exception, e:
            self._handle_exception(e)

    def test_start_nonauthorized(self):

        user = UserGenerator().generate()

        is_loggedin = self.client.login(
            username=user.username, password='invalid_pw')

        self.assertFalse(is_loggedin)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('Login' in response.content)  # redirect to login


class DownloadTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_csv_download(self):
        """ rest download of captable csv """

        # data
        company = CompanyGenerator().generate()
        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(
                company=company, number=str(x)))

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

        # run test
        response = self.client.get(
            reverse('captable_csv', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        with self.assertNumQueries(21):
            response = self.client.get(reverse('captable_csv',
                                       kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        lines = response.content.split('\r\n')
        lines.pop()  # remove last element based on final '\r\n'
        for row in lines:
            self.assertEqual(row.count(','), 6)
        self.assertEqual(len(lines), 3)  # ensure we have the right data
        # assert company itself
        self.assertEqual(shareholder_list[0].number, lines[1].split(',')[0])
        # assert share owner
        self.assertEqual(shareholder_list[1].number, lines[2].split(',')[0])
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
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(reverse('captable_csv',
                                   kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        lines = response.content.split('\r\n')
        lines.pop()  # remove last element based on final '\r\n'
        for row in lines:
            if row == lines[0]:  # skip first row
                continue
            self.assertEqual(row.count(','), 7)
            fields = row.split(',')
            s = Shareholder.objects.get(company=company, number=fields[0])
            text = s.current_segments(security)
            if text:
                self.assertTrue(text in fields[8])

    def test_csv_download_with_missing_operator(self):
        """ rest download of captable csv """

        # data
        company = CompanyGenerator().generate()
        shareholder_list = []
        for x in range(1, 6):  # don't statt with 0, Generators 'if' will fail
            shareholder_list.append(ShareholderGenerator().generate(
                company=company, number=str(x)))

        # initial share creation
        PositionGenerator().generate(
            buyer=shareholder_list[0], count=1000, value=10)
        # single transaction
        PositionGenerator().generate(
            buyer=shareholder_list[1], count=10, value=10,
            seller=shareholder_list[0])
        # shareholder bought and sold
        PositionGenerator().generate(buyer=shareholder_list[2], count=20,
                                     value=20, seller=shareholder_list[0])
        PositionGenerator().generate(buyer=shareholder_list[0], count=20,
                                     value=20, seller=shareholder_list[2])

        # run test
        response = self.client.get(
            reverse('captable_csv', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(
            reverse('captable_csv', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 403)

    def test_pdf_download(self):
        """ test download of captable pdf """
        company = CompanyGenerator().generate()
        # run test
        response = self.client.get(
            reverse('captable_pdf', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        with self.assertNumQueries(10):
            response = self.client.get(
                reverse('captable_pdf', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        self.assertTrue(response.content.startswith('%PDF-1.4\r\n'))
        self.assertTrue(response.content.endswith('EOF\r\n'))

    def test_pdf_download_with_number_segments(self):
        """ test download of captable pdf """
        company = CompanyGenerator().generate()
        secs = TwoInitialSecuritiesGenerator().generate(company=company)
        security = secs[1]
        security.track_numbers = True
        security.save()

        # login and retest
        user = UserGenerator().generate()
        OperatorGenerator().generate(user=user, company=company)
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(reverse('captable_pdf',
                                           kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 200)
        # assert proper csv
        self.assertTrue(response.content.startswith('%PDF-1.4\r\n'))
        self.assertTrue(response.content.endswith('EOF\r\n'))

    def test_pdf_download_with_missing_operator(self):
        """ test download of captable pdf """
        company = CompanyGenerator().generate()
        # run test
        response = self.client.get(
            reverse('captable_pdf', kwargs={"company_id": company.id}))

        # not logged in user
        self.assertEqual(response.status_code, 302)

        # login and retest
        user = UserGenerator().generate()
        is_loggedin = self.client.login(username=user.username,
                                        password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(is_loggedin)
        response = self.client.get(
            reverse('captable_pdf', kwargs={"company_id": company.id}))

        # assert response code
        self.assertEqual(response.status_code, 403)

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
        with self.assertNumQueries(29):
            res = _get_contacts(company)
        self.assertEqual(len(res), 11)
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
        with self.assertNumQueries(38):
            res = _get_transactions(
                from_date, to_date, Security.objects.first(), company)
        self.assertEqual(len(res), 17)
        self.assertEqual(len(res[0]), 11)
        self.assertEqual(len(res[1]), 9)  # no nationality
        self.assertEqual(res[0][0], _(u'date'))
