# coding=utf-8
import datetime
import logging

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.test import RequestFactory, TestCase
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from project.generators import (DEFAULT_TEST_DATA, CompanyGenerator,
                                CompanyShareholderGenerator,
                                ComplexOptionTransactionsWithSegmentsGenerator,
                                ComplexPositionsWithSegmentsGenerator,
                                ComplexShareholderConstellationGenerator,
                                OperatorGenerator, OptionTransactionGenerator,
                                PositionGenerator, SecurityGenerator,
                                ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator)
from project.tests.mixins import MoreAssertsTestCaseMixin
from services.rest.serializers import SecuritySerializer
from shareholder.models import (Operator, OptionTransaction, Position,
                                Security, Shareholder, OptionPlan, UserProfile)
from django.utils.translation import ugettext as _

logger = logging.getLogger()

User = get_user_model()


class AddCompanyTestCase(APITestCase):
    """
    test add company logic
    """
    def test_add_company(self):
        """
        confirm that we add all properly
        #54: common stock as default security
        """
        user = UserGenerator().generate()
        kwargs = {
            "name": "Pariatur Rerum est voluptates ipsa in officia libero "
                    "soluta omnis saepe voluptates omnis quidem autem veniam "
                    "rerum molestiae incidunt",
            "share_count": 36,
            "face_value": 18,
            "founded_at": "2016-05-31T23:00:00.000Z"
        }

        self.client.force_authenticate(user=user)
        res = self.client.post(reverse('add_company'), kwargs)

        self.assertEqual(res.status_code, 201)
        company = user.operator_set.all()[0].company
        self.assertEqual(company.security_set.all()[0].title, 'C')
        self.assertIsNotNone(self.client.session.get('company_pk'))

    def test_add_company_saving_twice(self):
        """
        confirm that we add all properly
        #54: common stock as default security
        """
        user = UserGenerator().generate()
        kwargs = {
            "name": "Pariatur Rerum est voluptates ipsa in officia libero "
                    "soluta omnis saepe voluptates omnis quidem autem veniam "
                    "rerum molestiae incidunt",
            "share_count": 36,
            "face_value": 18,
            "founded_at": "2016-05-31T23:00:00.000Z"
        }

        self.client.force_authenticate(user=user)
        res = self.client.post(reverse('add_company'), kwargs)

        self.assertEqual(res.status_code, 201)
        company = user.operator_set.all()[0].company
        username1 = company.get_company_shareholder().user.username
        self.assertEqual(company.security_set.all()[0].title, 'C')

        # second user
        user = UserGenerator().generate()
        self.client.force_authenticate(user=user)
        res = self.client.post(reverse('add_company'), kwargs)

        self.assertEqual(res.status_code, 201)
        company = user.operator_set.all()[0].company
        self.assertEqual(company.security_set.all()[0].title, 'C')
        username2 = company.get_company_shareholder().user.username
        self.assertEqual(username1[:25], username2[:-5])


class AvailableOptionSegmentsViewTestCase(APITestCase):

    def test_get(self):

        option_transactions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        optionplan = option_transactions[0].option_plan

        self.client.force_login(optionplan.company.operator_set.first().user)

        res = self.client.get(reverse('available_option_segments',
                                      kwargs={'shareholder_id': shs[0].pk,
                                              'optionsplan_id': optionplan.pk}))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [u'1201-1665', u'1667-2000'])

        res = self.client.get(reverse('available_option_segments',
                                      kwargs={'shareholder_id': shs[1].pk,
                                              'optionsplan_id': optionplan.pk}))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [u'1000-1200', 1666])


class CompanyViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.site = Site.objects.get_current()
        self.operator = OperatorGenerator().generate()

    def test_delete_company_permissions(self):
        """
        only auth'd operators can execute
        """
        # anon user
        response = self.client.delete(
            '/services/rest/company/{}'.format(self.operator.company.pk),
            **{'format': 'json'})

        self.assertEqual(response.status_code, 401)

        # operator
        self.client.force_login(self.operator.user)
        response = self.client.delete(
            '/services/rest/company/{}'.format(self.operator.company.pk),
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                self.operator.user.auth_token.key), 'format': 'json'})
        self.assertEqual(response.status_code, 204)

        # foreign operator
        op = OperatorGenerator().generate()
        self.client.force_login(op.user)
        response = self.client.delete(
            '/services/rest/company/{}'.format(self.operator.company.pk),
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                op.user.auth_token.key), 'format': 'json'})
        self.assertEqual(response.status_code, 404)

    def test_delete_company_and_related_data(self):
        """
        ensure related data is cleaned too, but not users and user profile
        """
        pk = self.operator.company.pk
        sh = ShareholderGenerator().generate(company=self.operator.company)
        uid = sh.user.pk
        puid = sh.user.userprofile.pk

        self.client.force_login(self.operator.user)
        response = self.client.delete(
            '/services/rest/company/{}'.format(self.operator.company.pk),
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                self.operator.user.auth_token.key), 'format': 'json'})
        self.assertEqual(response.status_code, 204)

        self.assertFalse(Shareholder.objects.filter(company__pk=pk).exists())
        self.assertFalse(Operator.objects.filter(company__pk=pk).exists())
        self.assertFalse(Position.objects.filter(
            Q(seller__company__pk=pk) | Q(buyer__company__pk=pk)
        ).exists())
        self.assertFalse(Security.objects.filter(company__pk=pk).exists())
        self.assertFalse(OptionPlan.objects.filter(company__pk=pk).exists())
        self.assertTrue(UserProfile.objects.filter(pk=puid).exists())
        self.assertTrue(User.objects.filter(pk=uid).exists())


class OperatorTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.site = Site.objects.get_current()

    def test_add_operator(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company
        user2 = UserGenerator().generate()

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "company": "http://{}/services/rest/company/"
            "{}".format(self.site.domain, company.pk),
            u"user": {'email': user2.email}
        }

        self.assertFalse(user2.operator_set.filter(company=company).exists())

        response = self.client.post(
            '/services/rest/operators',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue(user2.operator_set.filter(company=company).exists())

    def test_add_operator_wrong_email(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company
        user2 = UserGenerator().generate()

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "company": "http://{}/services/rest/company/"
            "{}".format(self.site.domain, company.pk),
            u"user": {"email": "a@a.de"}
        }

        self.assertFalse(user2.operator_set.filter(company=company).exists())

        response = self.client.post(
            '/services/rest/operators',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 400)
        self.assertTrue('email' in response.content)

    def test_add_operator_foreign_company(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = CompanyGenerator().generate()
        user2 = UserGenerator().generate()

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "company": "http://{}/services/rest/company/"
            "{}".format(self.site.domain, company.pk),
            u"user": {'email': user2.email}
        }

        self.assertFalse(user2.operator_set.filter(company=company).exists())

        response = self.client.post(
            '/services/rest/operators',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 400)
        self.assertTrue('company' in response.content)

    def test_delete_operator(self):
        operator = OperatorGenerator().generate()
        operator2 = OperatorGenerator().generate(company=operator.company)
        user = operator.user

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            u"operator.id": operator2.id}

        response = self.client.delete(
            '/services/rest/operators/{}'.format(operator2.pk),
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Operator.objects.filter(pk=operator2.pk).exists())


class PositionTestCase(MoreAssertsTestCaseMixin, TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_add_position(self):
        """ test that we can add a position """

        operator = OperatorGenerator().generate()
        user = operator.user

        buyer = ShareholderGenerator().generate(company=operator.company)
        seller = ShareholderGenerator().generate(company=operator.company)
        securities = TwoInitialSecuritiesGenerator().generate(
            company=operator.company)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "bought_at": "2016-05-13T23:00:00.000Z",
            "buyer": {
                "pk": buyer.pk,
                "user": {
                    "first_name": buyer.user.first_name,
                    "last_name": buyer.user.last_name,
                    "email": buyer.user.email,
                    "operator_set": [],
                    "userprofile": None,
                },
                "number": buyer.number,
                "company": {
                    "pk": operator.company.pk,
                    "name": operator.company.name,
                    "share_count": operator.company.share_count,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/"
                           "company/{}".format(operator.company.pk),
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "security": {
                "pk": securities[1].pk,
                "readable_title": "Preferred Stock",
                "title": "P",
                "count": 3,
                "face_value": 100
            },
            "count": 1,
            "value": 1,
            "seller": {
                "pk": seller.pk,
                "user": {
                    "first_name": seller.user.first_name,
                    "last_name": seller.user.last_name,
                    "email": seller.user.email,
                    "operator_set": [],
                    "userprofile": None
                },
                "number": seller.number,
                "company": {
                    "pk": 5,
                    "name": "LieblingzWaldCompany AG",
                    "share_count": 100100,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/company/5",
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "comment": "sdfg",
            "stock_book_id": "666",
            "depot_type": "1"
        }

        response = self.client.post(
            '/services/rest/position',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue('sdfg' in response.content)

        position = Position.objects.latest('id')
        self.assertEqual(position.count, 1)
        self.assertEqual(position.value, 1)
        self.assertEqual(position.buyer, buyer)
        self.assertEqual(position.seller, seller)
        self.assertEqual(position.registration_type, '2')
        self.assertEqual(
            position.bought_at.isoformat(), '2016-05-13')
        self.assertEqual(position.comment, "sdfg")
        self.assertEqual(position.stock_book_id, "666")
        self.assertEqual(position.depot_type, "1")

    def test_add_position_with_certificate_id(self):
        """ test that we can add a position """

        operator = OperatorGenerator().generate()
        user = operator.user

        buyer = ShareholderGenerator().generate(company=operator.company)
        seller = ShareholderGenerator().generate(company=operator.company)
        securities = TwoInitialSecuritiesGenerator().generate(
            company=operator.company)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "bought_at": "2016-05-13T23:00:00.000Z",
            "buyer": {
                "pk": buyer.pk,
                "user": {
                    "first_name": buyer.user.first_name,
                    "last_name": buyer.user.last_name,
                    "email": buyer.user.email,
                    "operator_set": [],
                    "userprofile": None,
                },
                "number": buyer.number,
                "company": {
                    "pk": operator.company.pk,
                    "name": operator.company.name,
                    "share_count": operator.company.share_count,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/"
                           "company/{}".format(operator.company.pk),
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "security": {
                "pk": securities[1].pk,
                "readable_title": "Preferred Stock",
                "title": "P",
                "count": 3,
                "face_value": 100
            },
            "count": 1,
            "value": 1,
            "certificate_id": '88888',
            "seller": {
                "pk": seller.pk,
                "user": {
                    "first_name": seller.user.first_name,
                    "last_name": seller.user.last_name,
                    "email": seller.user.email,
                    "operator_set": [],
                    "userprofile": None
                },
                "number": seller.number,
                "company": {
                    "pk": 5,
                    "name": "LieblingzWaldCompany AG",
                    "share_count": 100100,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/company/5",
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "comment": "sdfg",
            "stock_book_id": "666",
            "depot_type": "1"
        }

        response = self.client.post(
            '/services/rest/position',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue('sdfg' in response.content)

        position = Position.objects.latest('id')
        self.assertEqual(position.count, 1)
        self.assertEqual(position.value, 1)
        self.assertEqual(position.buyer, buyer)
        self.assertEqual(position.seller, seller)
        self.assertEqual(position.registration_type, '2')
        self.assertEqual(
            position.bought_at.isoformat(), '2016-05-13')
        self.assertEqual(position.comment, "sdfg")
        self.assertEqual(position.stock_book_id, "666")
        self.assertEqual(position.depot_type, "1")
        self.assertEqual(position.certificate_id, "88888")

    def test_add_position_with_number_segment(self):
        """
        test that we can add a position with numbered shares
        """

        operator = OperatorGenerator().generate()
        user = operator.user

        buyer = ShareholderGenerator().generate(company=operator.company)
        seller = ShareholderGenerator().generate(company=operator.company)
        securities = TwoInitialSecuritiesGenerator().generate(
            company=operator.company)
        PositionGenerator().generate(
            number_segments=[u'1-5'],
            company=operator.company, buyer=seller, count=5,
            security=securities[1])

        for s in securities:
            s.track_numbers = True
            s.save()

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "bought_at": "2016-05-13T23:00:00.000Z",
            "buyer": {
                "pk": buyer.pk,
                "user": {
                    "first_name": buyer.user.first_name,
                    "last_name": buyer.user.last_name,
                    "email": buyer.user.email,
                    "operator_set": [],
                    "userprofile": None,
                },
                "number": buyer.number,
                "company": {
                    "pk": operator.company.pk,
                    "name": operator.company.name,
                    "share_count": operator.company.share_count,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/"
                           "company/{}".format(operator.company.pk),
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "security": {
                "pk": securities[1].pk,
                "readable_title": "Preferred Stock",
                "title": "P",
                "count": 3,
                "face_value": 100
            },
            "count": 5,
            "value": 1,
            "seller": {
                "pk": seller.pk,
                "user": {
                    "first_name": seller.user.first_name,
                    "last_name": seller.user.last_name,
                    "email": seller.user.email,
                    "operator_set": [],
                    "userprofile": None
                },
                "number": seller.number,
                "company": {
                    "pk": 5,
                    "name": "LieblingzWaldCompany AG",
                    "share_count": 100100,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/company/5",
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "number_segments": "1,2,3-5",
            "comment": "sdfg"
        }

        response = self.client.post(
            '/services/rest/position',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue('sdfg' in response.content)
        self.assertEqual(response.data['number_segments'], [u'1-5'])

        position = Position.objects.latest('id')
        self.assertEqual(position.count, 5)
        self.assertEqual(position.value, 1)
        self.assertEqual(position.buyer, buyer)
        self.assertEqual(position.seller, seller)
        self.assertEqual(
            position.bought_at.isoformat(), '2016-05-13')
        self.assertEqual(position.number_segments, [u'1-5'])

    def test_add_position_with_number_segment_performance(self):
        """
        test that we can add a position with numbered shares
        """

        logger.info('preparing test...')
        operator = OperatorGenerator().generate()
        user = operator.user
        sec1, sec2 = TwoInitialSecuritiesGenerator().generate(
            company=operator.company)
        sec1.track_numbers = True
        sec1.number_segments = [u"1-10000000"]
        sec1.save()

        cs = CompanyShareholderGenerator().generate(
            security=sec1, company=operator.company)
        buyer = ShareholderGenerator().generate(company=operator.company)

        logger.info('data preparation done.')
        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "bought_at": "2016-05-13T23:00:00.000Z",
            "buyer": {
                "pk": buyer.pk,
                "user": {
                    "first_name": buyer.user.first_name,
                    "last_name": buyer.user.last_name,
                    "email": buyer.user.email,
                    "operator_set": [],
                    "userprofile": None,
                },
                "number": buyer.number,
                "company": {
                    "pk": operator.company.pk,
                    "name": operator.company.name,
                    "share_count": operator.company.share_count,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/"
                           "company/{}".format(operator.company.pk),
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100002,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "security": {
                "pk": sec1.pk,
                "title": sec1.title,
                "count": sec1.count,
                "track_numbers": True,
                "number_segments": sec1.number_segments,
                "face_value": sec1.face_value
            },
            "count": 1000000,
            "value": 0.5,
            "seller": {
                "pk": cs.pk,
                "user": {
                    "first_name": cs.user.first_name,
                    "last_name": cs.user.last_name,
                    "email": cs.user.email,
                    "operator_set": [],
                    "userprofile": None
                },
                "number": cs.number,
                "company": {
                    "pk": 5,
                    "name": "LieblingzWaldCompany AG",
                    "share_count": 100100,
                    "country": "",
                    "url": "http://codingmachine:9000/services/rest/company/5",
                    "shareholder_count": 2
                },
                "share_percent": "99.90",
                "share_count": 100000,
                "share_value": 1000020,
                "validate_gafi": {
                    "is_valid": True,
                    "errors": []
                }
            },
            "number_segments": "1-1000000",
            "comment": "Large Transaction"
        }

        # call with perf check
        # was 55, increased to 95
        with self.assertLessNumQueries(56):
            response = self.client.post(
                u'/services/rest/position',
                data,
                **{u'HTTP_AUTHORIZATION': u'Token {}'.format(
                    user.auth_token.key), u'format': u'json'})

        self.assertEqual(response.status_code, 201)
        self.assertTrue('Large Transaction' in response.content)
        self.assertEqual(response.data['number_segments'], [u'1-1000000'])

        position = Position.objects.latest('id')
        self.assertEqual(position.count, 1000000)
        self.assertEqual(position.value, 0.5)
        self.assertEqual(position.buyer, buyer)
        self.assertEqual(position.seller, cs)
        self.assertEqual(
            position.bought_at.isoformat(), '2016-05-13')
        self.assertEqual(position.number_segments, [u'1-1000000'])

    def test_delete_position(self):
        """
        operator deletes position
        """
        operator = OperatorGenerator().generate()
        user = operator.user
        position = PositionGenerator().generate(company=operator.company)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        res = self.client.delete(
            '/services/rest/position/{}'.format(position.pk))

        self.assertEqual(res.status_code, 204)
        self.assertFalse(Position.objects.filter(id=position.pk).exists())

    def test_delete_position_shareholder(self):
        """
        shareholder cannot delete positions
        """

        shareholder = ShareholderGenerator().generate()
        user = shareholder.user
        position = PositionGenerator().generate(company=shareholder.company)

        self.client.force_login(user)
        session = self.client.session
        session['company_pk'] = shareholder.company.pk
        session.save()

        res = self.client.delete(
            '/services/rest/position/{}'.format(position.pk))

        self.assertEqual(res.status_code, 403)

    def test_delete_confirmed_position(self):
        """
        confirmed positions cannot be deleted
        """
        operator = OperatorGenerator().generate()
        user = operator.user
        position = PositionGenerator().generate(company=operator.company)
        position.is_draft = False
        position.save()

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        res = self.client.delete(
            '/services/rest/position/{}'.format(position.pk))

        self.assertEqual(res.status_code, 400)

    def test_confirm_position(self):

        operator = OperatorGenerator().generate()
        user = operator.user
        seller = ShareholderGenerator().generate(company=operator.company)
        position = PositionGenerator().generate(seller=seller)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        # get and prep data
        res = self.client.login(username=user.username,
                                password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(res)

        res = self.client.get(
            '/services/rest/position/{}'.format(position.pk),
            format='json')

        # update data
        res = self.client.post(
            '/services/rest/position/{}/confirm'.format(position.pk),
            {},
            format='json'
            )

        self.assertEqual(res.status_code, 200)
        self.assertFalse(Position.objects.get(id=position.id).is_draft)

    def test_split_shares_GET(self):
        operator = OperatorGenerator().generate()
        user = operator.user

        ShareholderGenerator().generate(company=operator.company)
        ShareholderGenerator().generate(company=operator.company)
        TwoInitialSecuritiesGenerator().generate(company=operator.company)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)
        response = self.client.get(
            '/services/rest/split/', {},
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 405)

    def test_split_shares_POST(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company

        s1, s2 = TwoInitialSecuritiesGenerator().generate(
            company=operator.company)
        PositionGenerator().generate(company=operator.company, security=s1)
        PositionGenerator().generate(company=operator.company, security=s1)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        security = Security.objects.filter(company=company, title="P")[0]
        data = {
            'dividend': 3,
            'divisor': 4,
            "security": {
                "pk": security.pk,
                "readable_title": security.get_title_display(),
                "title": security.title
            },
            'execute_at': datetime.datetime.now(),
        }

        response = self.client.post(
            '/services/rest/split/', data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)

    def test_split_shares_empty_payload(self):
        operator = OperatorGenerator().generate()
        user = operator.user

        ShareholderGenerator().generate(company=operator.company)
        ShareholderGenerator().generate(company=operator.company)
        TwoInitialSecuritiesGenerator().generate(company=operator.company)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {}

        response = self.client.post(
            '/services/rest/split/', data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 400)
        self.assertTrue(len(response.data), 3)

    def test_search(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        position = PositionGenerator().generate(company=operator.company)

        self.client.force_login(user)

        query = position.buyer.user.first_name
        res = self.client.get(
            u'/services/rest/position?search={}'.format(query))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)

    def test_ordering(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        cs = CompanyShareholderGenerator().generate(company=operator.company)
        s1 = ShareholderGenerator().generate(company=operator.company)
        s2 = ShareholderGenerator().generate(company=operator.company)
        PositionGenerator().generate(company=operator.company, seller=cs,
                                     buyer=s1)
        PositionGenerator().generate(company=operator.company, seller=cs,
                                     buyer=s2)

        self.client.force_login(user)

        res = self.client.get(
            '/services/rest/position?ordering=buyer__user__last_name')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 3)
        last_names = [s.get('buyer')['full_name']
                      for s in res.data['results']]
        self.assertEqual(
            last_names,
            sorted(last_names, key=lambda s: s.split(' ')[1].lower()))

        res = self.client.get(
            '/services/rest/position?ordering=-buyer__number')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 3)
        numbers = [s.get('buyer')['number'] for s in res.data['results']]
        self.assertEqual(numbers, sorted(numbers, key=lambda s: s.lower(),
                         reverse=True))

    def test_pagination(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        cs = CompanyShareholderGenerator().generate(company=operator.company)
        s1 = ShareholderGenerator().generate(company=operator.company)
        s2 = ShareholderGenerator().generate(company=operator.company)
        PositionGenerator().generate(company=operator.company, seller=cs,
                                     buyer=s1)
        PositionGenerator().generate(company=operator.company, seller=cs,
                                     buyer=s2)

        self.client.force_login(user)

        res = self.client.get('/services/rest/position')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 3)
        self.assertEqual(res.data['current'], 1)
        self.assertEqual(len(res.data['results']), 3)


class ShareholderTestCase(TestCase):
    fixtures = ['initial.json']

    def setUp(self):
        self.client = APIClient()

    def test_invitee_invalid_email(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.post('/services/rest/invitee/',
                                    {"email": "kk.de"}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invitee_invalid_put_method(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.put('/services/rest/invitee/',
                                   {"email": "kk.de"}, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invitee_invalid_delete_method(self):

        # Using the standard RequestFactory API to create a form POST request
        response = self.client.delete('/services/rest/invitee/',
                                      {"email": "kk.de"}, format='json')

        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authenticate(self):
        """ authenticate, get token, and call for shareholder details """

        # prepare test data
        operator = OperatorGenerator().generate()
        shareholder = ShareholderGenerator().generate(company=operator.company)
        user = operator.user
        user.set_password('test')
        user.save()

        # authenticate
        response = self.client.post(
            '/services/rest/api-token-auth/',
            {'username': user.username, 'password': 'test'},
            format='json'
        )

        self.assertEqual(response.data.get('token'), user.auth_token.key)

        # get shareholder details
        token = user.auth_token
        session = self.client.session
        session['company_pk'] = operator.company.pk
        session.save()
        response = self.client.get(
            '/services/rest/shareholders',
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(token.key),
               'format': 'json'
               })

        self.assertTrue(len(response.data.get('results')) == 1)
        self.assertEqual(
            response.data['results'][0].get('full_name'),
            shareholder.get_full_name())

    def test_add_new_shareholder(self):
        """ addes a new shareholder and user and checks for special chars"""

        operator = OperatorGenerator().generate()
        user = operator.user

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            u"user": {
                u"first_name": u"Mike2Grüße",
                u"last_name": u"Hildebrand2Grüße",
                u"email": u"mike.hildebrand2@darg.com",
            },
            u"number": u"10002"}

        response = self.client.post(
            '/services/rest/shareholders',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data.get('user'), dict))
        self.assertEqual(response.data.get('number'), u'10002')
        self.assertEqual(User.objects.filter(email=user.email).count(), 1)

        # check proper db status
        user = User.objects.get(email="mike.hildebrand2@darg.com")

    def test_add_new_shareholder_without_email(self):
        """ addes a new shareholder and user and checks for special chars"""

        operator = OperatorGenerator().generate()
        user = operator.user

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            u"user": {
                u"first_name": u"Mike2Grüße",
                u"last_name": u"Hildebrand2Grüße",
            },
            u"number": u"10002"}

        response = self.client.post(
            '/services/rest/shareholders',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data.get('user'), dict))
        self.assertEqual(response.data.get('number'), u'10002')

        # check proper db status
        user = User.objects.get(first_name=u"Mike2Grüße")

    def test_add_duplicate_new_shareholder(self):
        """
        adds a new shareholder with same id
        """

        operator = OperatorGenerator().generate()
        shareholder = ShareholderGenerator().generate(company=operator.company)
        user = operator.user

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            u"user": {
                u"first_name": u"Mike2Grüße",
                u"last_name": u"Hildebrand2Grüße",
                u"email": u"mike.hildebrand2@darg.com",
            },
            u"number": shareholder.number}

        response = self.client.post(
            '/services/rest/shareholders',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data.get('number'),
            [_('Number must be unique for this company')]
        )

    def test_add_shareholder_for_existing_user_account(self):
        """ test to add a shareholder for an existing
        user account. means shareholder
        was added for another or same company already. means we don't
        add another user object
        """

        operator = OperatorGenerator().generate()
        user = operator.user

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "user": {
                "first_name": "Mike",
                "last_name": "Hildebrand",
                "email": "mike.hildebrand@darg.com",
            },
            "number": "1000"}

        response = self.client.post(
            '/services/rest/shareholders',
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data.get('user'), dict))
        self.assertEqual(response.data.get('number'), u'1000')
        self.assertEqual(User.objects.filter(email=user.email).count(), 1)

        # check proper db status
        user = User.objects.get(email="mike.hildebrand@darg.com")

    def test_edit_shareholder(self):
        """ test editing shareholder data
            required for editing:
            first_name, last_name
            email
            shareholder company name
            shareholder address (street, zip, city, province, country)
            birthday
        """
        operator = OperatorGenerator().generate()
        user = operator.user
        company = operator.company
        shareholder = ShareholderGenerator().generate(company=company)
        p = shareholder.user.userprofile
        p.language = "de"
        p.save()

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        data = {
            "pk": shareholder.user.pk,
            "mailing_type": '2',
            "user": {
                "first_name": "Mutter1Editable",
                "last_name": "KutterEditable",
                "email": shareholder.user.email,
                "operator_set": [],
                "userprofile": {
                    "street": "SomeStreet",
                    "city": "Hamm",
                    "province": "SomeProvince",
                    "postal_code": "932029",
                    "country": "http://codingmachine:9000/services/rest/"
                                "country/de",
                    "birthday": "2016-01-27T00:00:00.000Z",
                    "company_name": "SomeCompany",
                    "language": "ab",
                    "legal_type": 'H',
                    "street2": 'some street',
                    "company_department": 'dome depa',
                    "salutation": 'some saluta',
                    "title": 'some title',
                    "pobox": '12345',
                    "c_o": 'ddd',
                    "nationality": "http://codingmachine:9000/services/rest/"
                                   "country/de",
                },
            },
            "number": "00333e",
            "is_management": False,
            "company": {
                "pk": 5,
                "name": "LieblingzWaldCompany AG",
                "share_count": 100100,
                "country": "http://codingmachine:9000/services/rest"
                           "/country/DL",
                "url": "http://codingmachine:9000/services/rest/company/5",
                "shareholder_count": 2
            },
            "share_percent": "0.00",
            "share_count": 0,
            "share_value": 0,
            "validate_gafi": {
                "is_valid": True,
                "errors": []
            }
        }

        # call
        response = self.client.put(
            '/services/rest/shareholders/{}'.format(shareholder.pk),
            data,
            **{'HTTP_AUTHORIZATION': 'Token {}'.format(
                user.auth_token.key), 'format': 'json'})

        # assert
        s = Shareholder.objects.get(id=shareholder.id)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data.get('pk'), None)
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data.get('number'), "00333e")
        self.assertEqual(s.user.first_name, "Mutter1Editable")
        self.assertEqual(s.user.userprofile.language, "ab")
        self.assertEqual(s.mailing_type, u'2')

        userprofile = s.user.userprofile
        for k, v in data['user']['userprofile'].iteritems():
            if k == 'country':
                self.assertEqual(getattr(userprofile, k).pk, v[-2:])
                continue
            if k == 'birthday':
                self.assertEqual(
                    datetime.datetime.combine(
                        getattr(userprofile, k),
                        datetime.datetime.min.time()
                    ).isoformat(), v[:-5])
                continue
            if k == 'nationality':
                self.assertEqual(getattr(userprofile, k).iso_code, v[-2:])
                continue
            self.assertEqual(getattr(userprofile, k), v)

        # check proper db status
        user = s.user
        self.assertEqual(user.email, shareholder.user.email)

    def test_get_number_segments(self):
        """
        detailview to return owned segments for shareholder for all securities
        """
        positions, shs = ComplexPositionsWithSegmentsGenerator().generate()
        security = positions[0].security

        self.client.force_authenticate(
            shs[0].company.operator_set.all()[0].user)

        res = self.client.get(reverse('shareholders-number-segments',
                                      kwargs={'pk': shs[1].pk}))

        self.assertEqual(res.data[security.pk], [u'1000-1200', 1666])

    def test_get_list(self):
        """
        check list for performance and content
        """
        operator = OperatorGenerator().generate()
        user = operator.user
        ComplexShareholderConstellationGenerator().generate(
            company=operator.company, shareholder_count=100)

        self.client.force_login(user)

        res = self.client.get('/services/rest/shareholders')

        self.assertEqual(res.status_code, 200)
        # must have current page in meta payload
        self.assertIn('current', res.data.keys())
        # must have pagination
        self.assertEqual(len(res.data['results']), 20)

    def test_search(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        ComplexShareholderConstellationGenerator().generate(
            company=operator.company, shareholder_count=10)

        self.client.force_login(user)

        query = operator.company.shareholder_set.first().user.first_name
        res = self.client.get(
            '/services/rest/shareholders?search={}'.format(query))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)

        profile = operator.company.shareholder_set.first().user.userprofile
        profile.company_name = 'UniqueCompanyName88A'
        profile.save()

        res = self.client.get(
            '/services/rest/shareholders?search={}'.format(profile.company_name)
        )

        # FIXME assert failing randomly on CI. print for understandung the cause
        print res.data
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)

    def test_ordering(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        ComplexShareholderConstellationGenerator().generate(
            company=operator.company, shareholder_count=10)

        self.client.force_login(user)

        res = self.client.get(
            '/services/rest/shareholders?ordering=user__last_name')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 13)
        last_names = [s.get('full_name') for s in res.data['results']]
        self.assertEqual(
            last_names,
            sorted(last_names, key=lambda s: s.split(' ')[1].lower()))

        res = self.client.get(
            '/services/rest/shareholders?ordering=-number')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 13)
        numbers = [s.get('number') for s in res.data['results']]
        self.assertEqual(numbers, sorted(numbers, key=lambda s: s.lower(),
                         reverse=True))

    def test_pagination(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        ComplexShareholderConstellationGenerator().generate(
            company=operator.company, shareholder_count=30)

        self.client.force_login(user)

        res = self.client.get(
            '/services/rest/shareholders')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['current'], 1)
        self.assertEqual(len(res.data['results']), 20)

        res = self.client.get(res.data['next'])

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['current'], 2)
        self.assertEqual(len(res.data['results']), 13)

    def test_get_option_holders(self):
        op = OperatorGenerator().generate()
        opts = []
        for x in range(0, 10):
            opts.append(
                OptionTransactionGenerator().generate(company=op.company))

        self.client.force_authenticate(user=op.user)
        session = self.client.session
        session['company_pk'] = op.company.pk
        session.save()
        res = self.client.get(reverse(
            'shareholders-option-holder'), {'company': op.company.pk})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['results']), 10)

        # sell one persons options and check again
        ot = opts[0]
        OptionTransactionGenerator().generate(
            company=ot.option_plan.company, seller=ot.buyer, count=ot.count,
            price=1, buyer=opts[1].buyer)

        res = self.client.get(reverse(
            'shareholders-option-holder'), {'company': op.company.pk})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['results']), 9)

    def test_get_option_holders_search(self):
        op = OperatorGenerator().generate()
        opts = []
        for x in range(0, 10):
            opts.append(
                OptionTransactionGenerator().generate(company=op.company))

        self.client.force_authenticate(user=op.user)
        session = self.client.session
        session['company_pk'] = op.company.pk
        session.save()
        query = opts[0].buyer.user.first_name
        res = self.client.get(
            reverse('shareholders-option-holder'), {
                'company': op.company.pk,
                'search': query})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['results']), 1)
        self.assertIn(query, res.data['results'][0]['full_name'])


class OptionTransactionTestCase(APITestCase):

    def test_delete_option_transaction(self):
        """
        operator deletes position
        """
        operator = OperatorGenerator().generate()
        user = operator.user
        optiontransaction = OptionTransactionGenerator().generate(
            company=operator.company)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        res = self.client.delete(
            '/services/rest/optiontransaction/{}'.format(optiontransaction.pk))

        self.assertEqual(res.status_code, 204)
        self.assertFalse(
            OptionTransaction.objects.filter(id=optiontransaction.pk).exists())

    def test_delete_optiontransaction_shareholder(self):
        """
        shareholder cannot delete positions
        """

        operator = ShareholderGenerator().generate()
        user = operator.user
        optiontransaction = OptionTransactionGenerator().generate(
            company=operator.company)

        self.client.force_login(user)
        session = self.client.session
        session['company_pk'] = operator.company.pk
        session.save()

        res = self.client.delete(
            '/services/rest/optiontransaction/{}'.format(optiontransaction.pk))

        self.assertEqual(res.status_code, 403)

    def test_delete_confirmed_optiontransaction(self):
        """
        confirmed positions cannot be deleted
        """
        operator = OperatorGenerator().generate()
        user = operator.user
        optiontransaction = OptionTransactionGenerator().generate(
            company=operator.company)
        optiontransaction.is_draft = False
        optiontransaction.save()

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        res = self.client.delete(
            '/services/rest/optiontransaction/{}'.format(optiontransaction.pk))

        self.assertEqual(res.status_code, 400)

    def test_confirm_optiontransaction(self):

        operator = OperatorGenerator().generate()
        user = operator.user
        seller = ShareholderGenerator().generate(company=operator.company)
        optiontransaction = OptionTransactionGenerator().generate(
            seller=seller)

        logged_in = self.client.login(username=user.username,
                                      password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(logged_in)

        # get and prep data
        res = self.client.login(username=user.username,
                                password=DEFAULT_TEST_DATA['password'])
        self.assertTrue(res)

        res = self.client.get(
            '/services/rest/optiontransaction/{}'.format(optiontransaction.pk),
            format='json')

        # update data
        res = self.client.post(
            '/services/rest/optiontransaction/{}/confirm'.format(
                optiontransaction.pk),
            {},
            format='json'
            )

        self.assertEqual(res.status_code, 200)
        self.assertFalse(
            OptionTransaction.objects.get(id=optiontransaction.id).is_draft)

    def test_search(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        seller = ShareholderGenerator().generate(company=operator.company)
        optiontransaction = OptionTransactionGenerator().generate(
            seller=seller)

        self.client.force_login(user)

        query = optiontransaction.buyer.user.first_name
        res = self.client.get(
            '/services/rest/optiontransaction?search={}'.format(query))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)

        res = self.client.get(
            '/services/rest/optiontransaction?search={}'.format(
                optiontransaction.option_plan.title))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            res.data['count'],
            OptionTransaction.objects.filter(
                seller__company=operator.company
            ).count())
        self.assertNotEqual(res.data['count'], 0)

        optiontransaction.certificate_id = 'SOME STRANGE ID'
        optiontransaction.stock_book_id = 'MORE TEST STRINGS'
        optiontransaction.save()

        res = self.client.get(
            '/services/rest/optiontransaction?search={}'.format(
                optiontransaction.certificate_id))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)

        res = self.client.get(
            '/services/rest/optiontransaction?search={}'.format(
                optiontransaction.stock_book_id))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)

    def test_ordering(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        seller = ShareholderGenerator().generate(company=operator.company)
        o1 = OptionTransactionGenerator().generate(
            seller=seller)
        o2 = OptionTransactionGenerator().generate(
            seller=seller)

        self.client.force_login(user)

        res = self.client.get(
            '/services/rest/optiontransaction?ordering=seller__user__last_name')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 2)
        last_names = [s.get('seller')['full_name']
                      for s in res.data['results']]
        self.assertEqual(last_names,
                         sorted(last_names, key=lambda s: s.lower()))

        res = self.client.get(
            '/services/rest/optiontransaction?ordering=-seller__number')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 2)
        numbers = [s.get('seller')['number'] for s in res.data['results']]
        self.assertEqual(numbers, sorted(numbers, key=lambda s: s.lower(),
                         reverse=True))

        # default ordering by bought_at
        o1.bought_at = datetime.datetime(2014, 1, 1)
        o1.save()
        o2.bought_at = datetime.datetime(2013, 12, 31)
        o2.save()

        res = self.client.get(
            '/services/rest/optiontransaction')

        self.assertEqual(res.data['results'][0].get('pk'), o1.pk)
        self.assertEqual(res.data['results'][1].get('pk'), o2.pk)

    def test_pagination(self):
        operator = OperatorGenerator().generate()
        user = operator.user
        seller = ShareholderGenerator().generate(company=operator.company)
        OptionTransactionGenerator().generate(
            seller=seller)
        OptionTransactionGenerator().generate(
            seller=seller)

        self.client.force_login(user)

        res = self.client.get(
            '/services/rest/optiontransaction')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 2)
        self.assertEqual(res.data['current'], 1)
        self.assertEqual(len(res.data['results']), 2)


class SecurityTestCase(APITestCase):

    def setUp(self):
        super(SecurityTestCase, self).setUp()
        self.factory = RequestFactory()

    def test_save_number_segments(self):
        company = CompanyGenerator().generate()
        operator = OperatorGenerator().generate(company=company)
        security = SecurityGenerator().generate(company=company)
        url = reverse('security-detail', kwargs={'pk': security.id})
        request = self.factory.get(url)

        data = SecuritySerializer(security, context={'request': request}).data
        # segments must be double quoted as they are rendered to json as plain
        # string and the quotes will disappear
        data.update({'number_segments': '"1,2,3,4,8-10"'})
        del data['face_value']  # mandatory, remove

        self.client.force_authenticate(user=operator.user)
        session = self.client.session
        session['company_pk'] = company.pk
        session.save()

        res = self.client.put(url, data=data)
        self.assertIn('Vorzugsaktien', res.content)
        self.assertEqual(res.status_code, 200)

        security = Security.objects.get(id=security.id)
        self.assertEqual(security.number_segments, [u'1-4', u'8-10'])

        data.update({'number_segments': '"1,2,3,4,4,,8-10"'})

        res = self.client.put(url, data=data)

        self.assertEqual(res.status_code, 200)

        security = Security.objects.get(id=security.id)
        self.assertEqual(security.number_segments, [u'1-4', u'8-10'])
