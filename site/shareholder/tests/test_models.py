#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import datetime
import logging
import math
import os
import shutil
import tempfile
from decimal import Decimal

import mock
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.db.models import Q
from django.test import TestCase, TransactionTestCase, override_settings
from django.test.client import Client, RequestFactory
from django.utils import timezone
from django.utils.encoding import force_text
from model_mommy import mommy

from project.generators import (BankGenerator,
                                CompanyGenerator, CompanyShareholderGenerator,
                                ComplexOptionTransactionsWithSegmentsGenerator,
                                ComplexPositionsWithSegmentsGenerator,
                                ComplexShareholderConstellationGenerator,
                                MassPositionsWithSegmentsGenerator,
                                OperatorGenerator, OptionPlanGenerator,
                                OptionTransactionGenerator, PositionGenerator,
                                SecurityGenerator, ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator)
from project.tests.mixins import StripeTestCaseMixin, SubscriptionTestMixin
from shareholder.models import (Company, Country, Position, Security,
                                Shareholder, ShareholderStatement,
                                ShareholderStatementReport, UserProfile,
                                create_auth_token)

logger = logging.getLogger(__name__)


# --- MODEL TESTS
class SignalTestCase(TestCase):

    def _strip_related_user_objects(self, user):
        profile = user.userprofile
        profile.delete()
        token = user.auth_token
        token.delete()

    def test_create_auth_token_corp_user(self):
        """ signal must create api token and userprofile for new user obj """
        # use generator and remove token and user profile objs
        instance = UserGenerator().generate()
        self._strip_related_user_objects(instance)

        # make corp shareholder user
        instance.first_name = settings.COMPANY_INITIAL_FIRST_NAME
        instance.save()

        class Sender(object):
            pass

        create_auth_token(Sender(), instance=instance, created=True)

        instance = User.objects.get(pk=instance.pk)
        self.assertTrue(hasattr(instance, 'userprofile'))
        self.assertTrue(isinstance(instance.userprofile, UserProfile))
        profile = instance.userprofile
        profile.refresh_from_db()
        self.assertEqual(profile.legal_type, 'C')

    def test_create_auth_token_private_user(self):
        """ signal must create api token and userprofile for new user obj """
        # use generator and remove token and user profile objs
        instance = UserGenerator().generate()
        self._strip_related_user_objects(instance)

        class Sender(object):
            pass

        create_auth_token(Sender(), instance=instance, created=True)

        instance = User.objects.get(pk=instance.pk)
        profile = instance.userprofile
        profile.refresh_from_db()
        self.assertEqual(instance.userprofile.legal_type, 'H')


class CompanyTestCase(StripeTestCaseMixin, SubscriptionTestMixin, TestCase):

    def setUp(self):
        super(CompanyTestCase, self).setUp()

        self.company = CompanyGenerator().generate(share_count=10, vote_ratio=2)
        self.security = SecurityGenerator().generate(count=10, face_value=100,
                                                     company=self.company)

        self.shareholder1 = ShareholderGenerator().generate(
            company=self.company)
        self.shareholder2 = ShareholderGenerator().generate(
            company=self.company)
        self.position1 = PositionGenerator().generate(
            seller=None, buyer=self.shareholder1, security=self.security,
            count=10)
        self.position2 = PositionGenerator().generate(
            seller=self.shareholder1, buyer=self.shareholder2,
            security=self.security, count=2)
        optionplan = OptionPlanGenerator().generate(
            company=self.company, security=self.security)
        OptionTransactionGenerator().generate(seller=self.shareholder1,
                                              buyer=self.shareholder2,
                                              security=self.security, count=2,
                                              option_plan=optionplan)

    @mock.patch('shareholder.models.cache')
    def test_get_active_shareholders(self, cache_mock):
        """ return qs of active shareholders """
        cache_mock.get.return_value = None
        cache_key = 'company-{}-{}-none-active-shareholders'.format(
            self.company.pk, timezone.now().date())

        shs = self.company.get_active_shareholders()
        self.assertEqual(
            list(shs.order_by('number')),
            list(self.company.shareholder_set.all().order_by('number')))
        self.assertEqual(len(shs), 2)
        cache_mock.set.assert_called_with(cache_key, shs, 86400)

        # cache hit
        cache_mock.reset_mock()
        cache_mock.get.return_value = self.company.shareholder_set.all()
        shs = self.company.get_active_shareholders()
        self.assertEqual(list(shs.reverse()),
                         list(self.company.shareholder_set.all()))
        self.assertEqual(len(shs), 2)
        cache_mock.get.assert_called_with(cache_key)

        # kwargs used
        cache_mock.reset_mock()
        cache_mock.get.return_value = self.company.shareholder_set.all()
        shs = self.company.get_active_shareholders(date=timezone.now().date(),
                                                   security=self.security)
        self.assertEqual(list(shs.reverse()),
                         list(self.company.shareholder_set.all()))
        self.assertEqual(len(shs), 2)

        # kwargs used, ancient date
        cache_mock.reset_mock()
        cache_mock.get.return_value = self.company.shareholder_set.all()
        oneyearago = timezone.now().date() - relativedelta(years=1)
        shs = self.company.get_active_shareholders(date=oneyearago,
                                                   security=self.security)
        self.assertEqual(list(shs.reverse()),
                         list(self.company.shareholder_set.all()))

    def test_get_new_certificate_id(self):
        """
        get fresh unused cert id
        """
        self.assertEqual(self.company.get_new_certificate_id(), 1)

        self.position1.certificate_id = '1a'
        self.position1.save()
        self.assertEqual(self.company.get_new_certificate_id(), 2)

        self.position2.certificate_id = '99'
        self.position2.save()
        self.assertEqual(self.company.get_new_certificate_id(), 100)

    def test_get_new_shareholder_number(self):
        """ get new unused shareholder number """
        self.shareholder1.number = u'A23.B'
        self.shareholder1.save()
        self.shareholder2.number = u'98..'
        self.shareholder2.save()
        self.shareholder3 = ShareholderGenerator().generate(
            company=self.company)
        self.shareholder3.number = u'100'
        self.shareholder3.save()
        self.shareholder3.set_dispo_shareholder()

        self.assertEqual(self.company.get_new_shareholder_number(), 99)

    def test_text_repr(self):

        optiontransaction, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        company = shs[0].company
        company.name = u'Mühleggbahn AG'
        company.save()
        security = company.security_set.all()[0]
        force_text(security)  # must not raise exception

        company.name = u'UniCodeTestÄGå'
        company.save()
        # see https://goo.gl/8hEVWH
        force_text(security)  # must not raise exception

    def test_get_all_option_plan_segments(self):
        """
        retrieve list of all segments blocked by option plans
        """

        optiontransaction, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        company = shs[0].company
        security = company.security_set.all()[0]

        self.assertEqual(company.get_all_option_plan_segments(),
                         [u'1000-2000'])

        OptionPlanGenerator().generate(company=company, security=security,
                                       number_segments=[2222, u'3000-4011'])

        self.assertEqual(company.get_all_option_plan_segments(),
                         [2222, u'3000-4011', u'1000-2000'])

        OptionPlanGenerator().generate(security=security,
                                       number_segments=[5555])

        self.assertEqual(company.get_all_option_plan_segments(),
                         [2222, u'3000-4011', u'1000-2000'])

    def test_get_total_share_count_floating(self):
        """
        how many votes are owned by shareholders outside company
        """
        self.assertEqual(self.company.get_total_share_count_floating(), 2)

        ds = ShareholderGenerator().generate(company=self.company)
        ds.set_dispo_shareholder()
        PositionGenerator().generate(
            seller=self.shareholder1, security=self.security, count=1, buyer=ds)
        self.assertEqual(self.company.get_total_share_count_floating(), 2)

    def test_get_total_votes(self):
        """
        how many votes does a company have?
        """

        # should be 500
        self.assertEqual(self.company.get_total_votes(), 10*100/2)

    def test_get_total_votes_floating(self):
        """
        how many votes are owned by shareholders outside company
        """
        self.assertEqual(self.company.get_total_votes_floating(), 2*100/2)

        ds = ShareholderGenerator().generate(company=self.company)
        ds.set_dispo_shareholder()
        PositionGenerator().generate(
            seller=self.shareholder1, security=self.security, count=1, buyer=ds)
        self.assertEqual(self.company.get_total_votes_floating(), 2*100/2)

    @mock.patch('shareholder.models.select_template')
    def test_statement_template(self, mock_select_template):
        """
        get template for shareholder statements
        """
        self.company.get_statement_template()
        mock_select_template.assert_called_with([
            'pdf/statement.{}.pdf.html'.format(self.company.pk),
            'pdf/statement.pdf.html'
        ])

    def test_has_feature_enabled(self):
        self.assertFalse(self.company.has_feature_enabled('foo'))

        # add company subscription
        self.add_subscription(self.company)
        self.assertFalse(self.company.has_feature_enabled('foo'))
        self.assertTrue(self.company.has_feature_enabled('shareholders'))

    def test_get_current_subscription_plan(self):
        self.assertIsNone(self.company.get_current_subscription_plan())

        # add company subscription
        self.add_subscription(self.company)

        plan = self.company.get_current_subscription_plan()
        self.assertIsNotNone(plan)
        self.assertEqual(plan, 'test')

        plan_display = self.company.get_current_subscription_plan(display=True)
        self.assertEqual(plan_display, 'Test Plan')

    def test_get_current_subscription_plan_display(self):
        self.assertIsNone(self.company.get_current_subscription_plan_display())

        # add company subscription
        self.add_subscription(self.company)

        plan_display = self.company.get_current_subscription_plan_display()
        self.assertEqual(plan_display, 'Test Plan')

    def test_validate_plan(self):
        self.assertEqual(self.company.validate_plan('test'), (True, []))
        self.assertTrue(
            self.company.validate_plan('test', include_errors=False))

        plans = copy.deepcopy(settings.DJSTRIPE_PLANS)
        plans['test']['validators'] = [
            'company.validators.features.ShareholderCountPlanValidator'
        ]
        plans['test']['features']['shareholders']['max'] = 1
        with self.settings(DJSTRIPE_PLANS=plans):
            self.assertFalse(
                self.company.validate_plan('test', include_errors=False))

    def test_can_subscribe_plan(self):

        with mock.patch.object(self.company, 'validate_plan',
                               return_value=True):
            self.assertTrue(self.company.can_subscribe_plan('test'))

        with mock.patch.object(self.company, 'validate_plan',
                               return_value=False):
            self.assertFalse(self.company.can_subscribe_plan('test'))

    def test_subscription_features(self):
        self.assertEqual(self.company.subscription_features, [])

        # add company subscription
        self.add_subscription(self.company)

        self.assertEqual(self.company.subscription_features,
                         settings.ALL_FEATURES.keys())

    def test_subscription_permissions(self):
        self.assertEqual(self.company.subscription_permissions, [])

        # add company subscription
        self.add_subscription(self.company)

        plans = copy.deepcopy(settings.DJSTRIPE_PLANS)
        plans['test']['features']['shareholders']['max'] = 1
        plans['test']['features']['shareholders']['validators']['create'] = [
            'company.validators.features.ShareholderCreateMaxCountValidator'
        ]

        with self.settings(DJSTRIPE_PLANS=plans):
            self.assertNotIn('create_shareholders',
                             self.company.subscription_permissions)

        plans['test']['features']['shareholders']['max'] = 10

        with self.settings(DJSTRIPE_PLANS=plans):
            self.assertIn('create_shareholders',
                          self.company.subscription_permissions)

    def test_has_printed_certificates(self):
        ot = OptionTransactionGenerator().generate()
        self.assertFalse(ot.option_plan.company.has_printed_certificates())
        ot.printed_at = timezone.now()
        ot.save()
        self.assertTrue(ot.option_plan.company.has_printed_certificates())

    def test_has_vested_positions(self):
        ot = OptionTransactionGenerator().generate()
        self.assertFalse(ot.option_plan.company.has_vested_positions())
        ot.vesting_months = 22
        ot.save()
        self.assertTrue(ot.option_plan.company.has_vested_positions())


class CountryTestCase(TestCase):

    def test_model(self):

        Country.objects.create(iso_code='de', name="Germany")

        qs = Country.objects.all()
        country = qs[0]

        self.assertEqual(qs.count(), 1)
        self.assertEqual(country.iso_code, 'de')
        self.assertEqual(country.name, 'Germany')


class PositionTestCase(TransactionTestCase):

    def test_invalidate_certificate(self):
        """
        create a second position to invalidate a cert and return it
        to copmany depot
        """
        pos = PositionGenerator().generate(
            certificate_id='1234', depot_type='0',
            depot_bank=BankGenerator().generate())

        pos.invalidate_certificate()

        pos.refresh_from_db()

        self.assertIsNotNone(pos.certificate_invalidation_position)
        ipos = pos.certificate_invalidation_position
        self.assertEqual(ipos.certificate_id, pos.certificate_id)
        self.assertEqual(ipos.depot_bank, pos.depot_bank)
        self.assertEqual(ipos.depot_type, '1')

    def test_split_shares(self):
        """
        share split leaves value, percent unchanged but
        increases share count per shareholder
        """
        # test data
        company = CompanyGenerator().generate(share_count=1000)
        OperatorGenerator().generate(company=company)
        shareholders, security = ComplexShareholderConstellationGenerator()\
            .generate(company=company)

        data = {
            'execute_at': timezone.now(),
            'dividend': 3,
            'divisor': 7,
            'comment': "Some random comment",
            'security': security,
        }
        multiplier = float(data['divisor']) / float(data['dividend'])
        company_share_count = company.share_count

        # record initial shareholder asset status
        assets = {}
        for shareholder in shareholders:
            assets.update({
                shareholder.pk: {
                    'count': shareholder.share_count(),
                    'value': shareholder.share_value(),
                    'percent': shareholder.share_percent()
                }
            })

        # run
        company.split_shares(data)

        # asserts by checking overall shareholder situation
        # means each shareholder should have now more shares but some
        # overall stock value

        # company shareholder last...
        leftover = 0
        shareholders.reverse()
        for shareholder in shareholders:
            if shareholder == shareholders[-1]:
                pt, count2 = math.modf(assets[shareholder.pk]['count'] *
                                       multiplier)
                count2 += round(leftover)
            else:
                part, count2 = math.modf(
                    assets[shareholder.pk]['count'] * multiplier)
                leftover += part

            print shareholder
            print shareholder.buyer.all()
            print shareholder.seller.all()
            self.assertEqual(
                shareholder.share_count(),
                count2
            )

        self.assertEqual(
            company.share_count,
            round(company_share_count * multiplier))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(
            mail.outbox[0].subject,
            u"Ihre Liste gespaltener Aktienanrechte f\xfcr das Unternehmen "
            u"'{}'".format(company.name)
        )

    def test_split_shares_empty_value(self):
        """
        share split leaves value, percent unchanged but
        increases share count per shareholder
        """
        # test data
        company = CompanyGenerator().generate(share_count=1000)
        OperatorGenerator().generate(company=company)
        shareholders, security = ComplexShareholderConstellationGenerator()\
            .generate(company=company)
        # all positions have not value
        for position in Position.objects.all():
            position.value = None
            position.save()

        data = {
            'execute_at': timezone.now(),
            'dividend': 3,
            'divisor': 7,
            'comment': "Some random comment",
            'security': security,
        }
        multiplier = float(data['divisor']) / float(data['dividend'])
        company_share_count = company.share_count

        # record initial shareholder asset status
        assets = {}
        for shareholder in shareholders:
            assets.update({
                shareholder.pk: {
                    'count': shareholder.share_count(),
                    'value': shareholder.share_value(),
                    'percent': shareholder.share_percent()
                }
            })

        # run
        company.split_shares(data)

        # asserts by checking overall shareholder situation
        # means each shareholder should have now more shares but same
        # overall stock value

        leftover = 0
        shareholders.reverse()
        for shareholder in shareholders:
            if shareholder == shareholders[-1]:
                part, count2 = math.modf(assets[shareholder.pk]['count'] *
                                         multiplier)
                count2 += round(leftover)
            else:
                part, count2 = math.modf(
                    assets[shareholder.pk]['count'] * multiplier)
                leftover += part

            self.assertEqual(
                shareholder.share_count(),
                count2
            )

        self.assertEqual(
            company.share_count,
            round(company_share_count * multiplier))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(
            mail.outbox[0].subject,
            u"Ihre Liste gespaltener Aktienanrechte f\xfcr das Unternehmen "
            u"'{}'".format(company.name)
        )
        for position in Position.objects.all():
            self.assertIsNone(position.value)

    def test_split_shares_in_past(self):
        """
        we are splitting shares at some point in the past
        even with newer transactions entered
        approach: split in the very past and check that nothing was changed
        """
        # test data
        company = CompanyGenerator().generate(
            share_count=1000,
        )
        OperatorGenerator().generate(company=company)
        shareholders, security = ComplexShareholderConstellationGenerator()\
            .generate(
                company=company,
                company_shareholder_created_at='2013-1-1'
            )

        data = {
            'execute_at': timezone.make_aware(datetime.datetime(2014, 1, 1)),
            'dividend': 3,
            'divisor': 7,
            'comment': "Some random comment",
            'security': security,
        }
        company_share_count = company.share_count

        # record initial shareholder asset status
        assets = {}
        d = timezone.make_aware(datetime.datetime(2014, 1, 1))
        for shareholder in shareholders:
            assets.update({
                shareholder.pk: {
                    'count': shareholder.share_count(date=d),
                    'value': shareholder.share_value(date=d),
                    'percent': shareholder.share_percent(date=d)
                }
            })
        pcount = Position.objects.count()

        # run
        company.split_shares(data)

        # asserts by checking overall shareholder situation
        # means each shareholder should have now more shares but some
        # overall stock value
        cs = shareholders[0]
        mx = float(data['divisor']) / float(data['dividend'])
        for shareholder in shareholders:
            m = 1
            if shareholder.pk == cs.pk:
                m = mx
            self.assertEqual(
                shareholder.share_count(date=d),
                round(assets[shareholder.pk]['count'] * m)
            )

            # self.assertEqual(
            #     round(shareholder.share_value(date=d)),
            #     assets[shareholder.pk]['value']
            # )
            # self.assertEqual(
            #     round(float(shareholder.share_percent(date=d)), 2),
            #     float(assets[shareholder.pk]['percent'])
            # )

        self.assertEqual(
            company.share_count,
            round(company_share_count * mx))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(
            mail.outbox[0].subject,
            u"Ihre Liste gespaltener Aktienanrechte f\xfcr das Unternehmen "
            u"'{}'".format(company.name)
        )
        # only one new pos as no shares were basically existing as we
        # split even before company creates their first shares
        self.assertEqual(pcount + 2, Position.objects.count())

    def test_watter_split_61(self):
        """
        issue shares multiple times, sell some of them then do a split. see #61
        """
        company = CompanyGenerator().generate(share_count=10000000)
        sc = ShareholderGenerator().generate(company=company)  # aka Company
        s1 = ShareholderGenerator().generate(company=company)  # aka W
        s2 = ShareholderGenerator().generate(company=company)  # aka S
        OperatorGenerator().generate(company=company)
        security = SecurityGenerator().generate(company=company)
        now = timezone.now()
        PositionGenerator().generate(
            buyer=s2, seller=sc, count=10000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=11)
        )  # initial seed

        p1 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=187, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        p2 = PositionGenerator().generate(
            buyer=s1, seller=sc, count=398, value=100, security=security,
            bought_at=now-datetime.timedelta(days=9)
            )
        PositionGenerator().generate(
            buyer=s2, seller=s1, count=80, value=100, security=security,
            bought_at=now-datetime.timedelta(days=8)
            )
        PositionGenerator().generate(
            buyer=s2, seller=s1, count=437, value=100, security=security,
            bought_at=now-datetime.timedelta(days=7)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=837, value=100, security=security,
            bought_at=now-datetime.timedelta(days=6)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=68, value=100, security=security,
            bought_at=now-datetime.timedelta(days=5)
            )

        split_data = {
            'execute_at': now - datetime.timedelta(days=4),
            'dividend': 1,
            'divisor': 100,
            'comment': "MEGA SPLIT",
            'security': security,
        }
        company.split_shares(split_data)

        PositionGenerator().generate(
            buyer=s1, seller=sc, count=3350, value=100, security=security,
            bought_at=now-datetime.timedelta(days=3)
            )

        self.assertEqual(s1.share_count(), 100650)
        positions = Position.objects.filter(comment__contains="split").filter(
            Q(buyer=s1) | Q(seller=s1)
        )
        self.assertEqual(positions.count(), 2)
        p1 = positions[0]
        p2 = positions[1]
        self.assertEqual(p1.count, 973)
        self.assertEqual(p1.buyer, sc)
        self.assertEqual(p1.seller, s1)
        self.assertEqual(p2.count, 97300)
        self.assertEqual(p2.seller, sc)
        self.assertEqual(p2.buyer, s1)

    def test_can_view(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        buyer = ShareholderGenerator().generate(company=operator.company)
        seller = ShareholderGenerator().generate(company=operator.company)

        position = PositionGenerator().generate(seller=None, buyer=buyer)
        self.assertTrue(position.can_view(user))

        position = PositionGenerator().generate(seller=seller, buyer=buyer)
        self.assertTrue(position.can_view(user))


class UserProfileTestCase(TestCase):

    def test_model(self):

        user = UserGenerator().generate()
        profile = user.userprofile

        self.assertEqual(profile.country.iso_code, 'de')
        self.assertEqual(profile.country.name, 'Germany')
        self.assertEqual(profile.province, 'Some Province')


class SecurityTestCase(TestCase):

    def test_fields(self):
        security = SecurityGenerator().generate()

        self.assertTrue(hasattr(security, 'track_numbers'))
        self.assertTrue(hasattr(security, 'face_value'))
        self.assertTrue(hasattr(security, 'number_segments'))

        segments = [1, 2, 3, '4-6']
        security.number_segments = segments
        security.save()

        # refresh from db
        s = Security.objects.get(id=security.id)
        self.assertEqual(s.number_segments, segments)

    def test_count_in_segments(self):
        """
        count shares in segments
        """
        security = SecurityGenerator().generate()

        segments = '1, 3,4, 99-1000'
        count = security.count_in_segments(segments)
        self.assertEqual(count, 905)

        segments = [1, 3, 4, 5, u'99-1000']
        count = security.count_in_segments(segments)
        self.assertEqual(count, 906)

    def test_calculate_count(self):
        """
        how many shares are existing based on positions
        """
        company = CompanyGenerator().generate()
        security = SecurityGenerator().generate(company=company)
        # 1 cap increase and one sale position
        p1 = PositionGenerator().generate(company=company, seller=None,
                                          security=security, count=10)
        PositionGenerator().generate(company=company, count=2,
                                     security=security, seller=p1.buyer)

        self.assertEqual(security.calculate_count(), 10)

    def test_restricted_registered_shares(self):
        """
        we do have registered shares with restricted transferability
        """
        company = CompanyGenerator().generate()
        security = SecurityGenerator().generate(company=company)
        security.title = 'V'
        security.save()
        self.assertIn('Vinkuliert', security.get_title_display())


class ShareholderTestCase(TestCase):

    fixtures = ['initial.json']

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.company = CompanyGenerator().generate(share_count=10, vote_ratio=2)
        self.security = SecurityGenerator().generate(count=10, face_value=100,
                                                     company=self.company)

        self.shareholder1 = ShareholderGenerator().generate(
            company=self.company)
        self.shareholder2 = ShareholderGenerator().generate(
            company=self.company)
        PositionGenerator().generate(seller=None, buyer=self.shareholder1,
                                     security=self.security, count=10,
                                     bought_at=timezone.make_aware(
                                        datetime.datetime(2013, 1, 1)))
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=2)

    def test_cumulated_face_value(self):
        """
        calculate total face value invested
        """
        self.assertEqual(self.shareholder2.cumulated_face_value(),
                         Decimal('200.0000'))
        self.assertEqual(
            self.shareholder2.cumulated_face_value(security=self.security),
            Decimal('200.0000'))
        self.assertEqual(
            self.shareholder2.cumulated_face_value(
                security=self.security, date=timezone.make_aware(
                    datetime.datetime(2011, 1, 1))),
            Decimal('0.0000'))
        self.assertEqual(
            self.shareholder2.cumulated_face_value(
                security=self.security, date=timezone.make_aware(
                    datetime.datetime(2111, 1, 1))),
            Decimal('200.0000'))

        # one more sec
        self.security2 = SecurityGenerator().generate(count=10, face_value=100,
                                                      company=self.company)
        self.assertEqual(self.shareholder2.cumulated_face_value(),
                         Decimal('200.0000'))
        self.assertEqual(
            self.shareholder2.cumulated_face_value(security=self.security),
            Decimal('200.0000'))

    def test_current_segments(self):
        """
        get shareholders list of segments owned
        """
        positions, shs = ComplexPositionsWithSegmentsGenerator().generate()

        self.assertEqual(
            shs[1].current_segments(positions[0].security),
            [u'1000-1200', 1666])

    def test_current_segments_performance(self):
        """
        checks speed of method
        """
        poss, shs = MassPositionsWithSegmentsGenerator().generate()

        start = timezone.now()
        shs[0].current_segments(poss[0].security)
        end = timezone.now()
        delta = end-start
        self.assertLess(delta, datetime.timedelta(seconds=4))

    def test_current_options_segments(self):
        """
        which segments does a shareholder own via options
        """
        positions, shs = ComplexOptionTransactionsWithSegmentsGenerator()\
            .generate()

        self.assertEqual(
            shs[1].current_options_segments(positions[0].option_plan.security),
            [u'1000-1200', 1666])

        # test company shareholder
        self.assertEqual(
            shs[0].current_options_segments(positions[0].option_plan.security),
            [u'1201-1665', u'1667-2000'])

    def test_current_options_segments_same_day(self):
        """
        very simple scenario with one CS and one shareholder
        """
        company = CompanyGenerator().generate()
        OperatorGenerator().generate(company=company)

        # intial securities
        s1, s2 = TwoInitialSecuritiesGenerator().generate(company=company)
        s1.track_numbers = True
        s1.number_segments = [u'0001-2000']
        s1.save()

        # initial company shareholder
        cs = CompanyShareholderGenerator().generate(
            company=company, security=s1)
        s = ShareholderGenerator().generate(company=company)
        optionplan = OptionPlanGenerator().generate(
            company=company, number_segments=[u'1000-2000'], security=s1)
        # initial option grant to CompanyShareholder
        OptionTransactionGenerator().generate(
            company=company, security=s1, buyer=cs,
            number_segments=[u'1000-2000'], option_plan=optionplan)
        # single shareholder option grant
        OptionTransactionGenerator().generate(
            company=company, security=s1, buyer=s, seller=cs,
            number_segments=[u'1500-2000'], option_plan=optionplan)

        self.assertEqual(
            s.current_options_segments(s1),
            [u'1500-2000'])

        # test company shareholder
        self.assertEqual(
            cs.current_options_segments(s1),
            [u'1000-1499'])

    def test_current_options_segments_same_day_single_digit(self):
        """
        very simple scenario with one CS and one shareholder
        """
        company = CompanyGenerator().generate()
        OperatorGenerator().generate(company=company)

        # intial securities
        s1, s2 = TwoInitialSecuritiesGenerator().generate(company=company)
        s1.track_numbers = True
        s1.number_segments = [1, 2, 3, 4]
        s1.save()

        # initial company shareholder
        cs = CompanyShareholderGenerator().generate(
            company=company, security=s1)
        s = ShareholderGenerator().generate(company=company)
        optionplan = OptionPlanGenerator().generate(
            company=company, number_segments=[1, 2], security=s1)
        # initial option grant to CompanyShareholder
        OptionTransactionGenerator().generate(
            company=company, security=s1, buyer=cs,
            number_segments=[1, 2], option_plan=optionplan)
        # single shareholder option grant
        OptionTransactionGenerator().generate(
            company=company, security=s1, buyer=s, seller=cs,
            number_segments=[1], option_plan=optionplan)

        self.assertEqual(
            s.current_options_segments(s1),
            [1])

        # test company shareholder
        self.assertEqual(
            cs.current_options_segments(s1),
            [2])

    def test_get_management_share_count(self):
        """ get count of shares owned by management """
        self.shareholder1.is_management = True
        self.shareholder1.save()
        self.assertEqual(
            self.shareholder1.company.get_management_share_count(),
            self.shareholder1.share_count())

    def test_get_management_cumulated_face_value(self):
        """ get cumulated face value for all shares owned by management """
        self.shareholder1.is_management = True
        self.shareholder1.save()
        self.assertEqual(
            self.shareholder1.company.get_management_cumulated_face_value(),
            self.shareholder1.cumulated_face_value())

    def test_has_management(self):
        """ flag if company has shareholders marked as management """
        self.assertFalse(self.shareholder1.company.has_management())
        self.shareholder1.is_management = True
        self.shareholder1.save()
        self.assertTrue(self.shareholder1.company.has_management())

    def test_index(self):

        response = self.client.get("/", follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("Das Akt" in response.content)

    def test_is_company_shareholder(self):
        """
        is shareholder company shareholder?
        """
        s = ShareholderGenerator().generate()
        s2 = ShareholderGenerator().generate(company=s.company)
        self.assertTrue(s.is_company_shareholder())
        self.assertFalse(s2.is_company_shareholder())

    def test_has_vested_shares(self):
        shareholder3 = ShareholderGenerator().generate(
            company=self.company)
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=10,
                                     bought_at=timezone.make_aware(
                                        datetime.datetime(2013, 1, 1)),
                                     vesting_months=5)
        self.assertTrue(self.shareholder2.has_vested_shares())   # regular sh
        self.assertFalse(self.shareholder1.has_vested_shares())  # corp shareh
        self.assertFalse(shareholder3.has_vested_shares())       # fresh sh

    def test_owns_segments(self):
        """
        check if shareholder owns this list of segments. returns false on first
        fail
        """
        positions, shs = ComplexPositionsWithSegmentsGenerator().generate()
        segments = [1000, 1050, 1666, u'1103-1105']

        self.assertEqual(
            shs[1].owns_segments(segments, positions[0].security),
            (True, [], [u'1000-1200', 1666]))

        segments = [1000, 1050, 1666, 1667]

        self.assertEqual(
            shs[1].owns_segments(segments, positions[0].security),
            (False, [1667], [u'1000-1200', 1666]))

    def test_owns_segments_performance(self):
        """
        speed of segment owning check
        """
        poss, shs = MassPositionsWithSegmentsGenerator().generate()

        start = timezone.now()
        shs[0].owns_segments([10000-200000, 350000-800000], poss[0].security)
        end = timezone.now()
        delta = end - start
        if delta > datetime.timedelta(seconds=4):
            logger.error(
                'BUILD performance error: test_owns_segments_performance',
                extra={'delta': delta})
        self.assertLess(delta, datetime.timedelta(seconds=5))

    def test_owns_segments_rma_performance(self):
        """
        speed of segment owning check to meet RMA data
        """
        logger.info('preparing test...')
        operator = OperatorGenerator().generate()
        sec1, sec2 = TwoInitialSecuritiesGenerator().generate(
            company=operator.company)
        sec1.track_numbers = True
        sec1.number_segments = [u"1-10000000"]
        sec1.save()

        cs = CompanyShareholderGenerator().generate(
            security=sec1, company=operator.company)

        logger.info('data preparation done.')

        start = timezone.now()
        res = cs.owns_segments([u'1-582912'], sec1)
        end = timezone.now()
        delta = end - start
        self.assertTrue(res[0])
        if delta > datetime.timedelta(seconds=4):
            logger.error(
                'BUILD performance error: test_owns_segments_rma_performance',
                extra={'delta': delta})
        self.assertLess(delta, datetime.timedelta(seconds=7))

    def test_owns_options_segments(self):
        """
        does the user own this options segment?
        """
        positions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        security = positions[0].option_plan.security
        segments = [1000, 1050, 1666, u'1103-1105']

        self.assertEqual(
            shs[1].owns_options_segments(segments, security),
            (True, [], [u'1000-1200', 1666]))

        segments = [1000, 1050, 1666, 1667]

        self.assertEqual(
            shs[1].owns_options_segments(segments, security),
            (False, [1667], [u'1000-1200', 1666]))

    def test_share_count(self):
        """
        return number of shares owned by shareholder or available
        for sale by shareholder
        """
        now = timezone.now()
        yesterday = timezone.now() - datetime.timedelta(days=1)
        self.assertEqual(
            self.shareholder1.share_count(security=self.security), 8)
        self.assertEqual(
            self.shareholder2.share_count(security=self.security), 2)
        self.assertEqual(
            self.shareholder1.share_count(security=self.security, date=now), 8)
        self.assertEqual(
            self.shareholder2.share_count(security=self.security, date=now), 2)
        self.assertEqual(self.shareholder1.share_count(
            security=self.security, date=yesterday), 10)
        self.assertEqual(self.shareholder2.share_count(
            security=self.security, date=yesterday), 0)
        self.assertEqual(
            self.shareholder1.share_count(security=self.security, date=now,
                                          only_sellable=True), 8)
        self.assertEqual(
            self.shareholder2.share_count(security=self.security, date=now,
                                          only_sellable=True), 2)

    def test_share_count_without_vesting(self):
        """ count shares of shareholder which are not affected by any vesting
        """
        # add position with vesting
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=4,
                                     vesting_months=36)
        self.assertEqual(
            self.shareholder2.share_count(without_vesting=True), 2)

    def test_share_count_expired_vesting(self):
        """ count shares which have no vesting or where the vesting is expired

        scenario:
        * two owned without vesting (@setUp)
        * one owned with vesting expired
        * three owned with vesting not expired
        """
        oneyearago = timezone.now() - relativedelta(years=1)
        oneyearahead = timezone.now() + relativedelta(years=1)
        # unexpired
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=3,
                                     vesting_months=36, bought_at=oneyearago)
        # expired
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=1,
                                     vesting_months=6, bought_at=oneyearago)

        # one year ahead not to be calculated
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=1,
                                     vesting_months=6, bought_at=oneyearahead)

        # one sold in the past with vesting for the buyer
        PositionGenerator().generate(seller=self.shareholder2,
                                     buyer=self.shareholder1,
                                     security=self.security, count=1,
                                     vesting_months=6, bought_at=oneyearago)

        self.assertEqual(self.shareholder2.share_count(
            date=timezone.now().date(), expired_vesting=True), 2)

    def test_share_count_sellable(self):
        """ get count of shares sellable excluding vested shares and shares with
        certificate depot assigned
        """
        # sellable, no cert depot, no vesting @ setUp() with count=2

        # vesting only
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=1,
                                     vesting_months=6)

        # cert depot only
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=1,
                                     depot_type='0', certificate_id='9876')

        # vesting and cert depot
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=self.shareholder2,
                                     security=self.security, count=1,
                                     vesting_months=24, depot_type='0',
                                     certificate_id='987')

        self.assertEqual(self.shareholder2.share_count_sellable(), 2)

    def test_share_count_with_certificates(self):
        """
        respect sellable aspects of certificates for shares with cert depot at
        external banks
        """
        now = timezone.now()
        # valid certificate depot
        p1 = PositionGenerator().generate(seller=self.shareholder1,
                                          security=self.security, count=2,
                                          certificate_id='123453',
                                          depot_type='0')

        # issued and invalidated certificate
        p2 = PositionGenerator().generate(
            seller=self.shareholder1, security=self.security, count=3,
            certificate_id='98765', depot_type='0', buyer=self.shareholder2)
        p3 = PositionGenerator().generate(
            seller=p2.buyer, buyer=p2.buyer, security=self.security, count=3,
            certificate_id='98765', depot_type='1')
        p2.certificate_invalidation_position = p3
        p2.save()

        self.assertEqual(p1.buyer.share_count(security=self.security), 2)
        self.assertEqual(
            p1.buyer.share_count(security=self.security, only_sellable=True), 0)
        self.assertEqual(
            p1.buyer.share_count(security=self.security, only_sellable=True,
                                 date=now), 0)

        self.assertEqual(p2.buyer.share_count(security=self.security), 5)
        self.assertEqual(
            p2.buyer.share_count(security=self.security, only_sellable=True), 5)
        self.assertEqual(
            p2.buyer.share_count(security=self.security, only_sellable=True,
                                 date=now), 5)

    def test_share_percent(self):
        """
        proper share percent math
        """
        company = CompanyGenerator().generate(share_count=1000000)
        security = SecurityGenerator().generate(company=company)
        sc = ShareholderGenerator().generate(company=company)
        s1 = ShareholderGenerator().generate(company=company)
        s2 = ShareholderGenerator().generate(company=company)
        s3 = ShareholderGenerator().generate(company=company)
        now = timezone.now()

        PositionGenerator().generate(
            buyer=sc, count=1000000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=11)
            )
        PositionGenerator().generate(
            buyer=s1, seller=sc, count=500000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        PositionGenerator().generate(
            buyer=s2, seller=sc, count=5000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=9)
            )
        PositionGenerator().generate(
            buyer=s3, seller=sc, count=50, value=100, security=security,
            bought_at=now-datetime.timedelta(days=8)
            )

        self.assertEqual(s1.share_percent(), '99.00')
        self.assertEqual(s2.share_percent(), '0.99')
        self.assertEqual(s3.share_percent(), '0.01')

        PositionGenerator().generate(
            buyer=s2, seller=s1, count=250000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=7)
            )

        self.assertEqual(s1.share_percent(), '49.50')

    def test_share_value(self):
        """
        share value is last trated price
        """
        company = CompanyGenerator().generate(share_count=1000000)
        security = SecurityGenerator().generate(company=company)
        sc = ShareholderGenerator().generate(company=company)
        s1 = ShareholderGenerator().generate(company=company)
        now = timezone.now()

        PositionGenerator().generate(
            buyer=sc, count=1000000, value=1, security=security,
            bought_at=now-datetime.timedelta(days=11)
            )
        p = PositionGenerator().generate(
            buyer=s1, seller=sc, count=500000, value=100, security=security,
            bought_at=now-datetime.timedelta(days=10)
            )
        p.value = None
        p.save()

        self.assertEqual(s1.share_value(), Decimal('500000.0000'))

    def test_validate_gafi(self):
        """ test the gafi validation """

        # --- invalid street
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        shareholder.user.userprofile.street = ''
        shareholder.user.userprofile.save()

        self.assertFalse(shareholder.validate_gafi()['is_valid'])

        # --- invalid company name
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')
        shareholder.user.userprofile.legal_type = 'C'
        shareholder.user.userprofile.company_name = None
        shareholder.user.userprofile.save()

        self.assertFalse(shareholder.validate_gafi()['is_valid'])

        # company name not relevant for humans
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')
        shareholder.user.userprofile.legal_type = 'H'
        shareholder.user.userprofile.company_name = None
        shareholder.user.userprofile.save()

        self.assertTrue(shareholder.validate_gafi()['is_valid'])

        # --- valid data
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        self.assertTrue(shareholder.validate_gafi()['is_valid'])

    def test_validate_gafi_with_missing_userprofile(self):
        shareholder = ShareholderGenerator().generate()
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        profile = shareholder.user.userprofile
        profile.delete()

        shareholder = Shareholder.objects.get(id=shareholder.id)
        # must be in switzerland
        shareholder.company.country = Country.objects.get(
            iso_code__iexact='ch')

        self.assertFalse(hasattr(shareholder.user, 'userprofile'))
        self.assertFalse(shareholder.validate_gafi()['is_valid'])

    def test_vote_count(self):
        self.assertEqual(self.shareholder1.vote_count(), 400)  # corps sh
        self.assertEqual(self.shareholder2.vote_count(), 100)

    def test_vote_percent(self):
        self.assertEqual(self.shareholder1.vote_percent(), 0.0)
        self.assertEqual(self.shareholder2.vote_percent(), 1)

        shareholder3 = ShareholderGenerator().generate(
            company=self.company)
        PositionGenerator().generate(seller=self.shareholder1,
                                     buyer=shareholder3,
                                     security=self.security, count=2)
        self.assertEqual(self.shareholder2.vote_percent(), 0.5)
        self.assertEqual(shareholder3.vote_percent(), 0.5)

        shareholder4 = ShareholderGenerator().generate(
            company=self.company)
        PositionGenerator().generate(seller=self.shareholder2,
                                     buyer=shareholder4,
                                     security=self.security, count=1)
        self.assertEqual(self.shareholder2.vote_percent(), 0.25)
        self.assertEqual(shareholder3.vote_percent(), 0.5)
        self.assertEqual(shareholder4.vote_percent(), 0.25)


class ShareholderStatementReportTestCase(StripeTestCaseMixin,
                                         SubscriptionTestMixin, TestCase):

    TEST_DIR = os.path.join(tempfile.gettempdir(), '.dargtests')
    SHAREHOLDER_STATEMENT_ROOT = os.path.join(TEST_DIR, 'statements')

    @classmethod
    def tearDownClass(cls):
        super(ShareholderStatementReportTestCase, cls).tearDownClass()

        # remove tempdir
        shutil.rmtree(cls.TEST_DIR)

    def setUp(self):
        super(ShareholderStatementReportTestCase, self).setUp()

        self.company = CompanyGenerator().generate()
        self.report = mommy.make(ShareholderStatementReport,
                                 company=self.company, pdf_file='test.pdf')

    def test_statement_count(self):
        self.assertEqual(self.report.statement_count, 0)

        mommy.make(ShareholderStatement, report=self.report,
                   pdf_file='example.pdf', _quantity=3)

        self.assertEqual(self.report.statement_count, 3)

    def test_get_statement_sent_count(self):
        self.assertEqual(self.report.statement_sent_count, 0)

        now = timezone.now()
        mommy.make(ShareholderStatement, report=self.report,
                   pdf_file='example.pdf', email_sent_at=now, _quantity=2)

        self.assertEqual(self.report.statement_sent_count, 2)

    def test_get_statement_letter_count(self):
        self.assertEqual(self.report.statement_letter_count, 0)

        now = timezone.now()
        mommy.make(ShareholderStatement, report=self.report,
                   pdf_file='example.pdf', letter_sent_at=now, _quantity=2)

        self.assertEqual(self.report.statement_letter_count, 2)

    def test_get_statement_opened_count(self):
        self.assertEqual(self.report.statement_opened_count, 0)

        now = timezone.now()
        mommy.make(ShareholderStatement, report=self.report,
                   pdf_file='example.pdf', email_opened_at=now, _quantity=2)

        self.assertEqual(self.report.statement_opened_count, 2)

    def test_get_statement_downloaded_count(self):
        self.assertEqual(self.report.statement_downloaded_count, 0)

        now = timezone.now()
        mommy.make(ShareholderStatement, report=self.report,
                   pdf_file='example.pdf', pdf_downloaded_at=now, _quantity=2)

        self.assertEqual(self.report.statement_downloaded_count, 2)

    @mock.patch(
        'shareholder.models.ShareholderStatement.send_email_notification')
    @mock.patch(
        'shareholder.models.ShareholderStatementReport._create_joint_statements_pdf')  # noqa
    def test_generate_statements(self, mock_merge_pdfs, mock_email_notify):
        self.assertIsNone(self.company.statement_sending_date)

        with mock.patch.object(
                self.report, '_create_shareholder_statement_for_user') \
                as mock_statment_create:

            self.assertIsNone(self.report.generate_statements())
            mock_statment_create.assert_not_called()

            # add subscription
            self.add_subscription(self.company)

            today = timezone.now().date()
            self.company.statement_sending_date = today
            self.company.save()

            def side_effect(user):
                statement = mommy.make(ShareholderStatement, user=user,
                                       pdf_file='example.pdf')
                return (statement, True)

            mock_statment_create.side_effect = side_effect

            self.report.generate_statements()
            # no shareholders
            mock_statment_create.assert_not_called()
            company = Company.objects.get(pk=self.company.pk)
            self.assertEqual(
                company.statement_sending_date,
                (today + relativedelta(year=today.year + 1))
            )

            mommy.make(Shareholder, company=self.company, _quantity=3)

            self.report.generate_statements(send_notify=False)
            mock_statment_create.assert_called()
            mock_email_notify.assert_not_called()
            mock_merge_pdfs.assert_called()

            company = Company.objects.get(pk=self.company.pk)
            self.assertEqual(
                company.statement_sending_date,
                (today + relativedelta(year=today.year + 2))
            )

            self.report.generate_statements(send_notify=True)
            mock_email_notify.assert_called()

    @override_settings(SHAREHOLDER_STATEMENT_ROOT=SHAREHOLDER_STATEMENT_ROOT)
    def test_get_statement_pdf_path_for_user(self):
        shareholder = ShareholderGenerator().generate(company=self.company)
        path = self.report._get_statement_pdf_path_for_user(shareholder.user)
        self.assertIn(str(shareholder.user_id), path)
        self.assertIn(str(self.company.pk), path)
        self.assertIn(str(self.report.report_date.year), path)
        self.assertTrue(os.path.exists(path))
        self.assertTrue(os.path.isdir(path))

    @override_settings(SHAREHOLDER_STATEMENT_ROOT=SHAREHOLDER_STATEMENT_ROOT)
    def test_create_joint_statements_pdf(self):
        """ merge all pdfs with each other """
        user = UserGenerator().generate()
        shareholders = mommy.make(Shareholder, user=user, _quantity=2)
        PositionGenerator().generate(company=self.company,
                                     buyer=shareholders[0])
        statement, created = (
            self.report._create_shareholder_statement_for_user(user))
        self.report._create_joint_statements_pdf()
        self.report.refresh_from_db()
        self.assertIsNotNone(self.report.pdf_file)
        self.assertTrue(os.path.isfile(self.report.pdf_file))

        # test recreation
        os.remove(self.report.pdf_file)
        filepath = statement.pdf_file
        statement.delete()
        os.remove(filepath)

    @override_settings(SHAREHOLDER_STATEMENT_ROOT=SHAREHOLDER_STATEMENT_ROOT)
    def test_create_shareholder_statement_for_user(self):
        user = UserGenerator().generate()

        # no shareholders
        self.assertEqual(
            self.report._create_shareholder_statement_for_user(user),
            (None, False))

        # add shareholers for user
        shareholders = mommy.make(Shareholder, user=user, _quantity=2)

        # no shares/options
        self.assertEqual(
            self.report._create_shareholder_statement_for_user(user),
            (None, False))

        # add shares/options
        PositionGenerator().generate(company=self.company,
                                     buyer=shareholders[0])

        with mock.patch.object(self.report, '_create_statement_pdf',
                               return_value=False):
            with self.assertRaises(Exception):
                self.report._create_shareholder_statement_for_user(user)

        statement, created = (
            self.report._create_shareholder_statement_for_user(user))
        self.assertIsNotNone(statement)
        self.assertTrue(created)

        # test existing
        statement, created = (
            self.report._create_shareholder_statement_for_user(user))
        self.assertFalse(created)

        # test recreation
        filepath = statement.pdf_file
        statement.delete()

        statement, created = (
            self.report._create_shareholder_statement_for_user(user))
        self.assertIsNotNone(statement)
        self.assertTrue(created)
        self.assertEqual(filepath, statement.pdf_file)

        os.remove(filepath)
        self.assertFalse(os.path.isfile(statement.pdf_file))

        statement, created = (
            self.report._create_shareholder_statement_for_user(user))
        self.assertIsNotNone(statement)
        self.assertFalse(created)
        self.assertTrue(os.path.isfile(statement.pdf_file))

    @mock.patch('shareholder.models.render_pdf')
    def test_create_statement_pdf(self, mock_render_pdf):

        mock_render_pdf.side_effect = Exception()

        tfile = tempfile.NamedTemporaryFile(delete=False)

        self.assertFalse(self.report._create_statement_pdf(tfile.name, dict()))
        mock_render_pdf.assert_called()

        mock_render_pdf.reset_mock()
        mock_render_pdf.side_effect = None
        mock_render_pdf.return_value = 'PDFCONTENT'

        self.assertTrue(self.report._create_statement_pdf(tfile.name, dict()))
        self.assertTrue(os.path.isfile(tfile.name))

        # cleanup
        os.remove(tfile.name)

    def test_get_pdf_download_url(self):
        domain = Site.objects.get_current().domain

        url = self.report.pdf_download_url
        self.assertIn('file=', url)
        self.assertIn(domain, url)
        self.assertNotIn('&token=', url)

        url = self.report.get_pdf_download_url(
            absolute=False)
        self.assertIn('?file=', url)
        self.assertNotIn(domain, url)


class ShareholderStatementTestCase(TestCase):

    def setUp(self):
        super(ShareholderStatementTestCase, self).setUp()

        self.user = UserGenerator().generate()
        self.company = CompanyGenerator().generate()
        self.report = mommy.make(ShareholderStatementReport,
                                 company=self.company)
        self.statement = mommy.make(ShareholderStatement, pdf_file='test.pdf',
                                    user=self.user, report=self.report)

    @mock.patch('shareholder.tasks.send_statement_email.delay')
    def test_send_email_notification(self, mock_send_statement_email):
        self.assertIsNotNone(self.statement.user.email)
        self.statement.send_email_notification()
        mock_send_statement_email.assert_called()

        mock_send_statement_email.reset_mock()

        self.statement.user.email = ''
        with mock.patch.object(self.statement, 'send_letter') as mock_letter:
            self.statement.send_email_notification()
            mock_send_statement_email.assert_not_called()
            mock_letter.assert_called()

    @mock.patch('shareholder.tasks.send_statement_letter.delay')
    def test_send_letter(self, mock_send_statement_letter):
        self.statement.send_letter()
        mock_send_statement_letter.assert_called_with(self.statement.pk)

    def test_get_pdf_download_url(self):
        domain = Site.objects.get_current().domain

        url = self.statement.pdf_download_url
        self.assertIn('file=', url)
        self.assertIn(domain, url)
        self.assertNotIn('&token=', url)

        url = self.statement.get_pdf_download_url(
            absolute=False, with_auth_token=True)
        self.assertIn('?file=', url)
        self.assertNotIn(domain, url)
        self.assertIn('&token=', url)
