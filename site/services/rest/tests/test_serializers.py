#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase
from django.utils.translation import ugettext as _
from dateutil.parser import parse
from rest_framework.exceptions import ValidationError

from project.generators import (ComplexShareholderConstellationGenerator,
                                OperatorGenerator, OptionPlanGenerator,
                                OptionTransactionGenerator, PositionGenerator,
                                ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator,
                                ComplexPositionsWithSegmentsGenerator)
from services.rest.serializers import (AddCompanySerializer,
                                       OptionPlanSerializer,
                                       OptionTransactionSerializer,
                                       PositionSerializer,
                                       ShareholderSerializer,
                                       ShareholderListSerializer,
                                       UserProfileSerializer)
from shareholder.models import OptionPlan, OptionTransaction, Country, Position
from utils.formatters import human_readable_segments


class AddCompanySerializerTestCase(TestCase):

    def setUp(self):
        self.serializer = AddCompanySerializer()

    def test_create(self):
        validated_data = {
            'user': UserGenerator().generate(),
            'count': 33,
            'founded_at': datetime.datetime.now().date(),
            'name': u'Mühleggbahn AG',
            'face_value': 22,
        }
        res = self.serializer.create(validated_data)
        self.assertEqual(res, validated_data)


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


class PositionSerializerTestCase(TestCase):

    def __serialize(self, segments):
        position = PositionGenerator().generate(number_segments=segments,
                                                count=8)
        url = reverse('position-detail', kwargs={'pk': position.id})
        request = self.factory.get(url)
        # authenticated request
        request.user = OperatorGenerator().generate(
            company=position.buyer.company).user
        # prepare data
        data = PositionSerializer(
            position, context={'request': request}).data
        # clear bad datetimedata
        # data['buyer']['user']['userprofile']['birthday'] = None
        # data['seller']['user']['userprofile']['birthday'] = None
        data['bought_at'] = '2014-01-01T10:00'
        return (PositionSerializer(data=data, context={'request': request}),
                position)

    def setUp(self):
        self.factory = RequestFactory()

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

            # prepare data
            position.seller = None
            position.buyer = None
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
        self.assertIsNotNone(position_data['stock_book_id'])
        self.assertIsNotNone(position_data['depot_type'])


class ShareholderSerializerTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

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
        with self.assertNumQueries(130):  # should be < 12
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
        profile.birthday = datetime.datetime.now()
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
        profile.nationality = Country.objects.last()
        profile.save()
        request = self.factory.get('/services/rest/shareholders')
        request.user = operator.user

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

        # assure none is empty
        for k in profile_data.keys():
            self.assertIsNotNone(profile_data[k])


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
