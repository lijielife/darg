#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from decimal import Decimal

import mock
from dateutil.parser import parse
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase, Client
from django.utils import timezone
from django.utils.translation import ugettext as _
from rest_framework.exceptions import ValidationError

from project.generators import (BankGenerator, CompanyGenerator,
                                ComplexPositionsWithSegmentsGenerator,
                                ComplexShareholderConstellationGenerator,
                                OperatorGenerator, OptionPlanGenerator,
                                OptionTransactionGenerator, PositionGenerator,
                                ReportGenerator, SecurityGenerator,
                                ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator)
from project.tests.mixins import MoreAssertsTestCaseMixin, StripeTestCaseMixin
from services.rest.serializers import (AddCompanySerializer, BankSerializer,
                                       CompanySerializer, OperatorSerializer,
                                       OptionPlanSerializer,
                                       OptionTransactionSerializer,
                                       PositionSerializer, ReportSerializer,
                                       SecuritySerializer,
                                       ShareholderListSerializer,
                                       ShareholderSerializer,
                                       UserProfileSerializer, UserSerializer)
from shareholder.models import (Bank, Country, OptionPlan, OptionTransaction,
                                Position)
from utils.formatters import human_readable_segments
from utils.session import add_company_to_session


class AddCompanySerializerTestCase(TestCase):

    def setUp(self):
        url = reverse('add_company')
        self.request = RequestFactory().get(url)
        self.request.user = UserGenerator().generate()
        self.serializer = AddCompanySerializer(
            context={'request': self.request})

    def test_create(self):
        validated_data = {
            'user': self.request.user,
            'share_count': 33,
            'founded_at': timezone.now().date(),
            'name': u'Mühleggbahn AG',
            'face_value': 22,
        }
        company = self.serializer.create(validated_data)

        self.assertEqual(company.share_count, validated_data['share_count'])
        self.assertTrue(company.operator_set.filter(
                        user=validated_data['user']).exists())
        self.assertEqual(company.founded_at, validated_data['founded_at'])
        self.assertEqual(company.name, validated_data['name'])
        self.assertEqual(company.security_set.first().face_value,
                         validated_data['face_value'])
        self.assertEqual(company.shareholder_set.count(), 1)
        # IMPORTANT: email where invoice is sent to
        self.assertEqual(company.email, self.request.user.email)
        # check corp shareholder
        cs = company.get_company_shareholder()
        self.assertEqual(cs.user.email, u'')
        self.assertEqual(cs.user.userprofile.legal_type, u'C')

    def test_create_negative_share_count(self):
        """ see https://goo.gl/HDQB1t for users doing that """
        validated_data = {
            'user': UserGenerator().generate(),
            'share_count': -33,
            'founded_at': timezone.now().date(),
            'name': u'Mühleggbahn AG',
            'face_value': 22,
        }
        with self.assertRaises(ValidationError):
            self.serializer.validate_share_count(
                validated_data['share_count'])


class BankSerializerTestCase(TestCase):

    def setUp(self):
        self.bank = BankGenerator().generate()
        self.serializer = BankSerializer(instance=self.bank)

    def test_fields(self):
        serialized = self.serializer.data
        keys = ['pk', 'name', 'short_name', 'swift', 'address', 'city',
                'postal_code', 'full_name']
        self.assertEqual(serialized.keys(), keys)

    def test_get_full_name(self):
        name = self.serializer.get_full_name(self.bank)
        self.assertIn(self.bank.name, name)
        self.assertIn(self.bank.city, name)
        self.assertIn(self.bank.address, name)


class CompanySerializerTestCase(TestCase):

    def setUp(self):
        super(CompanySerializerTestCase, self).setUp()

        self.serializer = CompanySerializer()
        self.instance = CompanyGenerator().generate()

    def test_get_profile_url(self):
        url = self.serializer.get_profile_url(self.instance)
        self.assertEqual(url, reverse('company',
                                      kwargs={'company_id': self.instance.id}))


class OperatorSerializerTestCase(TestCase):

    def setUp(self):
        super(OperatorSerializerTestCase, self).setUp()

        self.serializer = OperatorSerializer()
        self.instance = OperatorGenerator().generate()
        self.factory = RequestFactory()

    def test_get_is_myself(self):
        req = self.factory.get('/')
        req.user = UserGenerator().generate()
        self.serializer.context = dict(request=req)
        self.assertFalse(self.serializer.get_is_myself(self.instance))

        req.user = self.instance.user
        self.serializer.context = dict(request=req)
        self.assertTrue(self.serializer.get_is_myself(self.instance))

    @unittest.skip('TODO: OperatorSerializer.create')
    def test_create(self):
        pass


class OptionPlanSerializerTestCase(TestCase):

    def __serialize(self, segments):
        seller = ShareholderGenerator().generate()
        option_plan = OptionPlanGenerator().generate(company=seller.company,
                                                     number_segments=segments,
                                                     count=8)
        PositionGenerator().generate(
            buyer=seller, count=8,
            number_segments=segments, security=option_plan.security)
        url = reverse('optionplan-detail', kwargs={'pk': option_plan.id})
        request = self.factory.get(url)
        request.user = OperatorGenerator().generate(
            company=option_plan.company).user
        request.session = {'company_pk': option_plan.company.pk}
        # prepare data
        data = OptionPlanSerializer(
            option_plan, context={'request': request}).data
        # clear bad datetimedata
        data['board_approved_at'] = '2014-01-01'
        return (
            OptionPlanSerializer(
                data=data, context={'request': request}
            ),
            option_plan)

    def setUp(self):
        self.factory = RequestFactory()

    def test_fields(self):
        """
        test field existuing
        """
        serializer = OptionPlanSerializer()
        self.assertTrue('readable_number_segments' in serializer.fields.keys())

    def test_create(self):
        """
        position serializer handling numbered shares
        """
        serializer, option_plan = self.__serialize('1, 3, 4, 6-9, 33')
        serializer.is_valid()
        sec = option_plan.security
        sec.track_numbers = True
        sec.save()
        res = serializer.create(serializer.initial_data)
        self.assertTrue(isinstance(res, OptionPlan))
        self.assertEqual(res.number_segments, [1, u'3-4', u'6-9', 33])
        self.assertEqual(res.optiontransaction_set.count(), 1)

    def test_is_valid(self):
        """
        option transaction serializer validation
        """

        serializer, option_plan = self.__serialize([1, 3, 4, u'6-9', 33])
        sec = option_plan.security
        sec.track_numbers = True
        sec.save()
        res = serializer.is_valid()
        self.assertEqual(res, True)

    def test_validate_pdf_file(self):
        serializer, option_plan = self.__serialize([1, 3, 4, u'6-9', 33])
        self.assertIsNone(serializer.validate_pdf_file(None))
        self.assertIsNone(serializer.validate_pdf_file(False))
        self.assertIsNone(serializer.validate_pdf_file(''))

        value = mock.Mock()
        content_type_mock = mock.PropertyMock(return_value='text/plain')
        type(value).content_type = content_type_mock

        with self.assertRaises(ValidationError):
            serializer.validate_pdf_file(value)

        content_type_mock = mock.PropertyMock(return_value='application/pdf')
        type(value).content_type = content_type_mock

        self.assertIsNotNone(serializer.validate_pdf_file(value))


class OptionTransactionSerializerTestCase(TestCase):

    def __serialize(self, segments):
        seller = ShareholderGenerator().generate()
        option_plan = OptionPlanGenerator().generate(company=seller.company,
                                                     number_segments=segments)
        # initial seeding
        OptionTransactionGenerator().generate(number_segments=segments, count=8,
                                              option_plan=option_plan,
                                              buyer=seller, seller=None)
        # to test transaction
        position = OptionTransactionGenerator().generate(
            number_segments=segments, count=8, seller=seller,
            option_plan=option_plan, save=False)
        url = reverse('optiontransaction-detail', kwargs={'pk': position.id})
        request = self.factory.get(url)
        request.user = OperatorGenerator().generate(
            company=option_plan.company).user
        request.session = {'company_pk': option_plan.company.pk}
        # prepare data
        data = OptionTransactionSerializer(
            position, context={'request': request}).data
        # clear bad datetimedata
        # data['buyer']['user']['userprofile']['birthday'] = None
        # data['seller']['user']['userprofile']['birthday'] = None
        data['bought_at'] = '2014-01-01'
        return (
            OptionTransactionSerializer(
                data=data, context={'request': request}
            ),
            position)

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.session = self.client.session

        self.transaction = OptionTransactionGenerator().generate()
        self.operator = OperatorGenerator().generate(
            company=self.transaction.buyer.company)

        add_company_to_session(self.session, self.operator.company)
        self.request = self.factory.get('/services/rest/position')
        self.request.user = self.operator.user
        self.request.session = self.session
        self.new_data = OptionTransactionSerializer(
            self.transaction, context={'request': self.request}).data
        self.new_data.update({'bought_at': '2013-05-05'})

    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_signal_on_create(self, signal_mock):
        self.new_data['depot_type'] = 1
        self.new_data['seller'] = self.new_data['buyer']
        serializer = OptionTransactionSerializer(
                data=self.new_data, context={'request': self.request})
        serializer.is_valid()
        obj = serializer.create(serializer.validated_data)
        calls = (mock.call(obj.buyer.pk))
        signal_mock.apply_async.has_calls(calls)

    def test_fields(self):
        """
        test field existuing
        """
        serializer = OptionTransactionSerializer()
        self.assertTrue('readable_number_segments' in serializer.fields.keys())
        self.assertIn('stock_book_id', serializer.fields.keys())
        self.assertIn('depot_type', serializer.fields.keys())

    def test_is_valid(self):
        """
        option transaction serializer validation
        """

        serializer, position = self.__serialize([1, 3, 4, u'6-9', 33])
        sec = position.option_plan.security
        sec.track_numbers = True
        sec.save()
        res = serializer.is_valid()
        self.assertEqual(res, True)

    def test_create(self):
        """
        position serializer handling numbered shares
        """
        serializer, position = self.__serialize('1, 3, 4, 6-9, 33')
        serializer.is_valid()
        sec = position.option_plan.security
        sec.track_numbers = True
        sec.save()
        res = serializer.create(serializer.validated_data)
        self.assertTrue(isinstance(res, OptionTransaction))
        self.assertEqual(res.number_segments, [1, u'3-4', u'6-9', 33])
        self.assertEqual(res.registration_type, '2')

    def test_get_readable_number_segments(self):

        serializer, position = self.__serialize([1, 3, 4, u'6-9', 33])
        result = serializer.get_readable_number_segments(position)
        self.assertNotIn('[', result)
        self.assertNotIn(']', result)
        self.assertNotIn('u', result)
        self.assertNotIn('{', result)
        self.assertNotIn('}', result)

    @unittest.skip('PLACEHOLDER - test for signal fired once implemented')
    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_update(self, signal_mock):
        serializer = OptionTransactionSerializer(
            data=self.new_data, context={'request': self.request})
        serializer.is_valid()
        obj = serializer.update(self.position, serializer.validated_data)
        signal_mock.apply_async.assert_called_with([obj.pk])

    def test_validate_certificate_id(self):
        """ certificate id must be unique """
        serializer, position = self.__serialize('1, 3, 4, 6-9, 33')
        certificate_id = '222'
        self.assertEqual(serializer.validate_certificate_id(certificate_id),
                         certificate_id)
        # OptionTransaction existing -> fail
        ot = OptionTransactionGenerator().generate(
            certificate_id=certificate_id, company=position.buyer.company)
        with self.assertRaises(ValidationError):
            serializer.validate_certificate_id(certificate_id)
        ot.delete()

        # Position existing -> fail
        position.certificate_id = certificate_id
        position.save()
        with self.assertRaises(ValidationError):
            serializer.validate_certificate_id(certificate_id)

    def test_validate_count(self):
        """ count must be positive and more then what shareholder owns """
        serializer, position = self.__serialize('1, 3, 4, 6-9, 33')
        certificate_id = '222'

        # negative count -> fail
        with self.assertRaises(ValidationError):
            self.assertEqual(serializer.validate_count(-1),
                             certificate_id)

        # less then shareholder owns -> fail
        with self.assertRaises(ValidationError):
            serializer.validate_count(
                position.seller.options_count(
                    security=position.option_plan.security) + 1)

        # success
        count = position.seller.options_count(
            security=position.option_plan.security)
        self.assertEqual(count, serializer.validate_count(count))


class PositionSerializerTestCase(TestCase):

    def __serialize(self, segments):
        # create capital
        bank = BankGenerator().generate()
        p = PositionGenerator().generate(number_segments=segments,
                                         count=8, seller=None)
        # position under test:
        position = PositionGenerator().generate(number_segments=segments,
                                                count=8,
                                                company=p.buyer.company,
                                                seller=p.buyer, save=False,
                                                security=p.security,
                                                depot_bank=bank)
        url = reverse('position-detail', kwargs={'pk': position.id})
        request = self.factory.get(url)
        # authenticated request
        request.user = OperatorGenerator().generate(
            company=position.buyer.company).user
        request.session = {'company_pk': position.buyer.company.pk}
        # prepare data
        data = PositionSerializer(
            position, context={'request': request}).data
        data['bought_at'] = '2024-01-01T10:00'
        return (PositionSerializer(data=data, context={'request': request}),
                position)

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.session = self.client.session

        self.position = PositionGenerator().generate(seller=None)
        self.operator = OperatorGenerator().generate(
            company=self.position.buyer.company)

        add_company_to_session(self.session, self.operator.company)
        self.request = self.factory.get('/services/rest/position')
        self.request.user = self.operator.user
        self.request.session = self.session
        self.new_data = PositionSerializer(
            self.position, context={'request': self.request}).data
        self.new_data.update({'bought_at': '2013-05-05T00:00'})

    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_create(self, signal_mock):
        del self.new_data['seller']
        del self.new_data['depot_bank']
        self.new_data['depot_type'] = 1
        serializer = PositionSerializer(data=self.new_data,
                                        context={'request': self.request})
        serializer.is_valid()
        obj = serializer.create(serializer.validated_data)
        calls = (mock.call(obj.buyer.pk))
        signal_mock.apply_async.has_calls(calls)

    def test_get_certificate_invalidation_position_url(self):
        """
        return url for cert invalidation position
        """
        pos = PositionGenerator().generate()
        pos.invalidate_certificate()

        serializer = PositionSerializer(instance=pos)
        self.assertIsNotNone(
            serializer.get_certificate_invalidation_position_url(pos))

        pos = PositionGenerator().generate()
        serializer = PositionSerializer(instance=pos)
        self.assertIsNone(
            serializer.get_certificate_invalidation_position_url(pos))

    def test_get_certificate_invalidation_initial_position_url(self):
        """
        return url for initial position for an cert invalidation
        """
        pos = PositionGenerator().generate()
        pos.invalidate_certificate()
        pos2 = pos.certificate_invalidation_position

        serializer = PositionSerializer(instance=pos)
        self.assertIsNotNone(
            serializer.get_certificate_invalidation_initial_position_url(pos2))

        pos = PositionGenerator().generate()
        serializer = PositionSerializer(instance=pos)
        self.assertIsNone(
            serializer.get_certificate_invalidation_initial_position_url(pos))

    def test_get_is_certificate_valid(self):
        """
        is certificate valid or was it returned
        """
        pos = PositionGenerator().generate()
        pos.invalidate_certificate()
        pos2 = pos.certificate_invalidation_position

        serializer = PositionSerializer(instance=pos)
        self.assertFalse(
            serializer.get_is_certificate_valid(pos))
        self.assertFalse(
            serializer.get_is_certificate_valid(pos2))

        pos = PositionGenerator().generate()
        serializer = PositionSerializer(instance=pos)
        self.assertIsNone(
            serializer.get_is_certificate_valid(pos))

        pos = PositionGenerator().generate(certificate_id='123')
        serializer = PositionSerializer(instance=pos)
        self.assertTrue(
            serializer.get_is_certificate_valid(pos))

    def test_is_valid(self):
        """
        position serializer handling numbered shares
        """
        serializer, position = self.__serialize([1, 3, 4, u'6-9', 33])
        res = serializer.is_valid()
        self.assertEqual(res, True)

    def test_is_valid_fail_segment_used_with_optionplan(self):
        """
        position serializer handling numbered shares failes due to segment
        used with option plan
        """
        segments = [1, 3, 4, u'6-9', 33]
        serializer, position = self.__serialize(segments)
        security = position.security
        security.track_numbers = True
        security.save()

        OptionPlanGenerator().generate(
            company=position.security.company,
            security=position.security,
            number_segments=segments
        )

        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid()

        self.assertEqual(cm.exception.detail.keys(), ['number_segments'])

    def test_create_capital_increase_numbered_shares(self):
        """
        position serializer handling numbered shares while doing a capital
        increase
        """
        def serialize(segments):
            operator = OperatorGenerator().generate()
            company = operator.company
            securities = TwoInitialSecuritiesGenerator().generate(
                company=company)
            security = securities[1]
            security.track_numbers = True
            security.save()
            position = PositionGenerator().generate(
                company=company, number_segments=segments, save=False,
                security=security, count=8)

            url = reverse('position-detail', kwargs={'pk': position.id})
            request = self.factory.get(url)
            request.user = operator.user
            request.session = {'company_pk': company.pk}

            # prepare data
            position.seller = None
            position.buyer = None
            position.depot_bank = BankGenerator().generate()
            # get test data dict
            data = PositionSerializer(
                position, context={'request': request}).data
            # clear bad datetimedata
            data['bought_at'] = '2014-01-01T10:00'
            del data['seller'], data['buyer']
            # feed data into serializer
            return PositionSerializer(data=data, context={'request': request})

        segments = [1, 3, 4, u'6-9', 33]
        serializer = serialize(human_readable_segments(segments))
        serializer.is_valid()
        position = serializer.create(serializer.validated_data)
        self.assertEqual(
            [1, u'3-4', u'6-9', 33],
            position.security.number_segments)
        self.assertEqual(position.registration_type, '1')
        self.assertEqual(position.depot_bank, Bank.objects.first())

    def test_fields(self):
        operator = OperatorGenerator().generate()
        poss, shs = ComplexPositionsWithSegmentsGenerator().generate(
            company=operator.company)  # does +2shs
        request = self.factory.get('/services/rest/shareholders')
        request.user = operator.user

        qs = Position.objects.filter(pk__in=[pos.pk for pos in poss])
        serializer = PositionSerializer(
            qs, many=True, context={'request': request})

        self.assertTrue(len(serializer.data) > 0)
        position_data = serializer.data[0]
        keys = position_data.keys()
        self.assertIsNotNone(position_data['stock_book_id'])
        self.assertIsNotNone(position_data['depot_type'])
        self.assertIn('depot_bank', keys)
        self.assertIn('certificate_invalidation_position_url', keys)
        self.assertIn('certificate_invalidation_initial_position_url', keys)
        self.assertIn('is_certificate_valid', keys)

    @unittest.skip('PLACEHOLDER - test for signal fired once implemented')
    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_update(self, signal_mock):
        serializer = PositionSerializer(data=self.new_data,
                                        context={'request': self.request})
        serializer.is_valid()
        obj = serializer.update(self.position, serializer.validated_data)
        signal_mock.apply_async.assert_called_with([obj.pk])

    def test_validate_certificate_id(self):
        """ certificate id must be unique """
        serializer, position = self.__serialize('1, 3, 4, 6-9, 33')
        certificate_id = '222'
        self.assertEqual(serializer.validate_certificate_id(certificate_id),
                         certificate_id)
        # OptionTransaction existing -> fail
        ot = OptionTransactionGenerator().generate(
            certificate_id=certificate_id, company=position.buyer.company)
        with self.assertRaises(ValidationError):
            serializer.validate_certificate_id(certificate_id)
        ot.delete()

        # Position existing -> fail
        position.certificate_id = certificate_id
        position.save()
        with self.assertRaises(ValidationError):
            serializer.validate_certificate_id(certificate_id)

    def test_validate_count(self):
        """ count must be positive and more then what shareholder owns """
        serializer, position = self.__serialize('1, 3, 4, 6-9, 33')
        certificate_id = '222'

        # negative count -> fail
        with self.assertRaises(ValidationError):
            self.assertEqual(serializer.validate_count(-1),
                             certificate_id)

        # less then shareholder owns -> fail
        with self.assertRaises(ValidationError):
            serializer.validate_count(
                position.seller.share_count(security=position.security) + 1)

        # success
        count = position.seller.share_count(security=position.security)
        self.assertEqual(count, serializer.validate_count(count))

    def test_validate_depot_bank(self):
        """
        force depot banks set if that is depot type 0 (cert depot)
        """
        serializer, position = self.__serialize('1, 3, 4, 6-9, 33')

        serializer.initial_data['depot_type'] = '1'
        self.assertEqual(serializer.validate_depot_bank(dict()), {})

        serializer.initial_data['depot_type'] = '0'
        self.assertEqual(serializer.validate_depot_bank('somevalue'),
                         'somevalue')

        with self.assertRaises(ValidationError):
            serializer.validate_depot_bank(None)


class ReportSerializerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.report = ReportGenerator().generate()
        url = reverse('reports:download', kwargs={'report_id': self.report.pk})
        self.request = self.factory.get(url)
        self.serializer = ReportSerializer(
            instance=self.report, context={'request': self.request})
        self.serialized_data = self.serializer.data

    def test_get_url(self):
        """ render url for download report """
        self.report.render()
        self.report.refresh_from_db()
        self.assertEqual(self.serializer.get_url(self.report),
                         '/reports/{}/download'.format(self.report.pk))

    def test_fields(self):
        """ do all fields respond properly """
        self.report.downloaded_at = timezone.now()
        self.report.generated_at = timezone.now()
        self.serializer = ReportSerializer(
            instance=self.report, context={'request': self.request})
        self.serialized_data = self.serializer.data
        for field in self.serializer.fields.keys():
            self.assertIsNotNone(self.serialized_data.get(field))


class ShareholderSerializerTestCase(MoreAssertsTestCaseMixin,
                                    StripeTestCaseMixin, TestCase):

    def setUp(self):
        super(ShareholderSerializerTestCase, self).setUp()

        self.factory = RequestFactory()
        self.client = Client()
        self.session = self.client.session

        self.shareholder = ShareholderGenerator().generate()
        self.operator = OperatorGenerator().generate(
            company=self.shareholder.company)

        add_company_to_session(self.session, self.operator.company)
        self.request = self.factory.get('/services/rest/shareholders')
        self.request.user = self.operator.user
        self.request.session = self.session
        self.new_data = ShareholderSerializer(
            self.shareholder, context={'request': self.request}).data
        self.new_data.update(
            {'number': self.operator.company.get_new_shareholder_number()})
        self.new_data['user']['userprofile'].update(
            {'birthday': '2013-05-05T00:00'})

    def test_is_company(self):

        s = ShareholderGenerator().generate()
        s2 = ShareholderGenerator().generate(company=s.company)
        self.assertTrue(ShareholderSerializer(s).get_is_company(s))
        self.assertFalse(ShareholderSerializer(s2).get_is_company(s2))

    def test_list_performance(self):
        """
        avoid query nightmare...
        """
        operator = OperatorGenerator().generate()
        shs, security = ComplexShareholderConstellationGenerator().generate(
            company=operator.company, shareholder_count=5)  # does +2shs
        request = self.factory.get('/services/rest/shareholders')
        request.user = operator.user

        # make sure we don't issue more then one additional query per obj
        with self.assertLessNumQueries(130):  # should be < 12
            # queryset with prefetch to reduce db load
            qs = operator.company.shareholder_set.all() \
                .select_related('company', 'user', 'user__userprofile',
                                'company__country') \
                .prefetch_related('user__operator_set', 'company__security_set',
                                  'company__shareholder_set') \
                .distinct()
            serializer = ShareholderListSerializer(
                qs, many=True, context={'request': request})
            self.assertTrue(len(serializer.data) > 0)

    def test_fields(self):
        """
        ensure all required fields are there
        """
        operator = OperatorGenerator().generate()
        shs, security = ComplexShareholderConstellationGenerator().generate(
            company=operator.company, shareholder_count=5)  # does +2shs
        profile = shs[0].user.userprofile
        profile.language = 'de'
        profile.country = Country.objects.first()
        profile.birthday = timezone.now()
        profile.street = 'some street'
        profile.street2 = 'some street'
        profile.city = 'some city'
        profile.province = ' some province'
        profile.postal_code = 'some postal code'
        profile.company_name = 'company some'
        profile.company_department = 'dome depa'
        profile.salutation = 'some saluta'
        profile.title = 'some title'
        profile.pobox = '12345'
        profile.c_o = 'ddd'
        profile.initial_registration_at = timezone.now()
        profile.nationality = Country.objects.last()
        profile.save()
        request = self.factory.get('/services/rest/shareholders')
        request.user = operator.user
        request.session = {'company_pk': operator.company.pk}

        qs = operator.company.shareholder_set.filter(pk=shs[0].pk)
        serializer = ShareholderSerializer(
            qs, many=True, context={'request': request})

        self.assertTrue(len(serializer.data) > 0)
        # shortcut to merge user and company name
        self.assertIsNotNone(serializer.data[0].get('full_name'))
        profile_data = serializer.data[0].get('user').get('userprofile')
        profile = qs[0].user.userprofile
        self.assertEqual(profile_data['title'], profile.title)
        self.assertEqual(profile_data['salutation'], profile.salutation)
        self.assertEqual(profile_data['street'], profile.street)
        self.assertEqual(profile_data['street2'], profile.street2)
        self.assertEqual(profile_data['pobox'], profile.pobox)
        self.assertEqual(profile_data['c_o'], profile.c_o)
        self.assertEqual(profile_data['country'][-2:], profile.country.iso_code)
        self.assertEqual(profile_data['language'], profile.language)
        self.assertEqual(profile_data['nationality'][-2:],
                         profile.nationality.iso_code)
        self.assertEqual(parse(profile_data['birthday']).date(),
                         profile.birthday)
        self.assertEqual(profile_data['postal_code'], profile.postal_code)
        self.assertEqual(profile_data['city'], profile.city)
        self.assertEqual(serializer.data[0]['mailing_type'], qs[0].mailing_type)
        self.assertEqual(serializer.data[0]['cumulated_face_value'],
                         Decimal(shs[0].cumulated_face_value()))

        # assure none is empty
        for k in profile_data.keys():
            self.assertIsNotNone(profile_data[k])

    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_create(self, signal_mock):
        serializer = ShareholderSerializer(data=self.new_data,
                                           context={'request': self.request})
        serializer.is_valid()
        sh = serializer.create(serializer.validated_data)
        signal_mock.apply_async.assert_called_with([sh.pk])

    @unittest.skip('TODO: ShareholderSerializer.is_valid')
    def test_is_valid(self):
        pass

    @mock.patch('shareholder.signals.update_order_cache_task')
    def test_update(self, signal_mock):
        serializer = ShareholderSerializer(data=self.new_data,
                                           context={'request': self.request})
        serializer.is_valid()
        sh = serializer.update(self.shareholder, serializer.validated_data)
        signal_mock.apply_async.assert_called_with([sh.pk])

    def test_validate_number(self):
        """
        shareholder.number must be unique
        """
        operator = OperatorGenerator().generate()
        shs, security = ComplexShareholderConstellationGenerator().generate(
            company=operator.company, shareholder_count=5)  # does +2shs
        request = self.factory.get('/services/rest/shareholders')
        request.user = operator.user
        request.session = {'company_pk': operator.company.pk}

        # existing number
        serializer = ShareholderSerializer(
            shs[1], context={'request': request})
        with self.assertRaises(ValidationError):
            serializer.validate_number(shs[0].number)

        # new number
        serializer = ShareholderSerializer(
            shs[1], context={'request': request})
        # no validationerror raised
        serializer.validate_number('345tfdw34rtf')


class SecuritySerializerTestCase(TestCase):

    def setUp(self):
        super(SecuritySerializerTestCase, self).setUp()

        self.serializer = SecuritySerializer()

    def test_get_get_readable_title(self):
        obj = SecurityGenerator().generate()

        obj.face_value = 100
        self.assertIn(obj.get_title_display(),
                      self.serializer.get_readable_title(obj))
        self.assertIn(str(obj.face_value),
                      self.serializer.get_readable_title(obj))

        obj.face_value = 0
        self.assertEqual(self.serializer.get_readable_title(obj),
                         obj.get_title_display())

    def test_get_readable_number_segments(self):
        obj = SecurityGenerator().generate()

        obj.number_segments = u'[1,2,4-10, {}]'
        result = self.serializer.get_readable_number_segments(obj)
        self.assertNotIn('[', result)
        self.assertNotIn(']', result)
        self.assertNotIn('u', result)
        self.assertNotIn('{', result)
        self.assertNotIn('}', result)

    def test_update(self):
        obj = SecurityGenerator().generate()

        obj = self.serializer.update(obj, dict())
        self.assertEqual(obj.number_segments, list())

        data = dict(number_segments='[1,2,4-10]')
        obj = self.serializer.update(obj, data)
        self.assertEqual(obj.number_segments, data.get('number_segments'))


class UserProfileSerializerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserGenerator().generate()
        request = self.factory.get('services/rest/user')
        self.serializer = UserProfileSerializer(self.user.userprofile,
                                                context={'request': request})

    def test_fields(self):
        self.assertEqual(self.serializer.data.get('readable_legal_type'),
                         _('Human Being'))
        self.assertEqual(self.serializer.data.get('legal_type'), 'H')


class UserSerializerTestCase(TestCase):

    def setUp(self):
        super(UserSerializerTestCase, self).setUp()

        self.serializer = UserSerializer()

    @unittest.skip('TODO: UserSerializer.create')
    def test_create(self):
        pass
