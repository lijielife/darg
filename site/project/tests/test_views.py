#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django.utils.translation import ugettext as _
from rest_framework.test import APIClient

from project.generators import (DEFAULT_TEST_DATA,
                                UserGenerator)
from project.tests.mixins import SubscriptionTestMixin
from shareholder.models import UserProfile


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


class TrackingTestCase(TestCase, SubscriptionTestMixin):

    def setUp(self):
        self.client = Client()

    def test_tracking(self):

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

        self.client.force_login(user)

        self.add_subscription(user.operator_set.first().company)

        response = self.client.get(reverse('start'), follow=True)

        self.assertEqual(response.status_code, 200)
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
