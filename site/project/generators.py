#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import hashlib
import logging
import random

from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as __
from model_mommy import random_gen

from shareholder.models import (Company, Country, Operator, OptionPlan,
                                OptionTransaction, Position, Security,
                                Shareholder, UserProfile)
from utils.formatters import inflate_segments
from utils.user import make_username

logger = logging.getLogger(__name__)

User = get_user_model()

DEFAULT_TEST_DATA = {
    'password': u'testàäå',
    'username': u'testusernameàäå',
    'date': u'13. Mai 2016',  # datepicker format
    'title': u'2016 OptionsPlan àäå',
    'exercise_price': u'2.05',
    'share_count': u'156',
    'comment': u'2345àäå',
    'security': __(u'Preferred Stock'),
    'count': u'2222',
    'vesting_period': 3,
    'number_segments': u'2100, 2101, 2102-2255',
    'company_name': u'SuperStart àäå AG',
    'value': u'4.55',
}


def _make_wordlist():

    words = [unicode(line.strip(), 'utf-8') for line in
             open('/usr/share/dict/american-english')]
    return words


def _make_user():

    words = _make_wordlist()
    hash_user = hashlib.sha1()
    # update method only accepts ascii
    hash_user.update(
        random.choice(words).encode('ascii', 'ignore') + str(
            random.randint(0, 100000))
    )
    username = hash_user.hexdigest()[0:25]
    email = "{}@{}".format(username, 'example.com')

    user = User.objects.create(
        is_active=True,
        first_name=random.choice(words),
        last_name=random.choice(words),
        username=username,
        email=email,
    )

    country, created = Country.objects.get_or_create(
        iso_code="de", defaults={"name": "Germany", "iso_code": "de"})

    # reload user to get the userprofile created by signal too
    user = User.objects.get(id=user.id)
    UserProfile.objects.filter(user=user).update(**dict(
        country=country,
        street="Some Street",
        city="SomeCity",
        province="Some Province",
        postal_code="12345",
        birthday=datetime.datetime.now(),
        company_name="SomeCorp"
        )
    )

    user.set_password(DEFAULT_TEST_DATA.get('password'))
    user.save()

    return user


class CompanyGenerator(object):

    def generate(self, **kwargs):

        word = random.choice(_make_wordlist())
        name = kwargs.get('name') or u'{} àäå A.B.'.format(word)
        share_count = kwargs.get('share_count') or 3
        country = kwargs.get('country') or CountryGenerator().generate()

        kwargs2 = {
            "name": name,
            "share_count": share_count,
            "country": country,
            "founded_at": datetime.datetime.now().date()
        }

        company = Company.objects.create(**kwargs2)

        return company


class SecurityGenerator(object):

    def generate(self, **kwargs):
        company = kwargs.get('company', CompanyGenerator().generate())
        kwargs2 = dict(title='P', company=company, count=1)
        kwargs2.update(kwargs)
        s1 = Security.objects.create(**kwargs2)

        return s1


class CountryGenerator(object):

    def generate(self):
        country, created = Country.objects.get_or_create(
            iso_code="de", defaults={"name": "Germany", "iso_code": "de"})
        return country


class UserGenerator(object):
    """ generate plain user """

    def generate(self):
        user = _make_user()

        return user


class OperatorGenerator(object):

    def generate(self, **kwargs):

        word = random.choice(_make_wordlist())
        user = kwargs.get("user") or _make_user()

        company = kwargs.get("company") or \
            CompanyGenerator().generate(
                name=u'{} A.B.'.format(word),
                share_count=3,
            )

        operator = Operator.objects.create(
            user=user,
            company=company,
        )

        return operator


class ShareholderGenerator(object):

    def generate(self, **kwargs):

        words = _make_wordlist()

        number = kwargs.get('number') or random.choice(words)+"234543"
        user = kwargs.get('user') or _make_user()
        company = kwargs.get('company') or CompanyGenerator().generate()
        mailing_type = kwargs.get('mailing_type') or 1

        shareholder = Shareholder.objects.create(
            user=user,
            number=number,
            company=company,
            mailing_type=mailing_type
        )

        return shareholder


class CompanyShareholderGenerator(object):

    def generate(self, **kwargs):

        company = kwargs.get('company') or CompanyGenerator().generate()
        company_shareholder_created_at = kwargs.get(
            'company_shareholder_created_at'
        ) or datetime.datetime.now()
        email = 'info@{}-company-itself.com'.format(slugify(company.name))
        companyuser = User.objects.create(
            username=make_username('Company', 'itself', email),
            first_name='Company', last_name='itself',
            email=email
        )
        shareholder = Shareholder.objects.create(
            user=companyuser,
            company=company,
            number='0')

        if kwargs.get('security') and kwargs.get('security').track_numbers:
            number_segments = kwargs.get('security').number_segments
        else:
            number_segments = []

        pos_kwargs = kwargs.copy()
        pos_kwargs.update({
            'buyer': shareholder,
            'count': company.share_count,
            'bought_at': company_shareholder_created_at,
            'seller': None,
            'number_segments': number_segments
        })

        PositionGenerator().generate(**pos_kwargs)

        return shareholder


class PositionGenerator(object):

    def generate(self, **kwargs):
        company = kwargs.get('company')
        if not company and kwargs.get('buyer'):
            company = kwargs.get('buyer').company
        if not company and kwargs.get('seller'):
            company = kwargs.get('seller').company
        if not company and kwargs.get('security'):
            company = kwargs.get('security').company
        if not company:
            company = CompanyGenerator().generate()

        buyer = kwargs.get('buyer') or ShareholderGenerator().generate(
            company=company)

        # seller only if not sent as kwarg
        if 'seller' not in kwargs.keys():
            seller = ShareholderGenerator().generate(company=company)
        else:
            seller = kwargs.get('seller')

        count = kwargs.get('count') or 3
        value = kwargs.get('value') or 2
        security = kwargs.get('security') or SecurityGenerator().generate(
            company=company)
        bought_at = kwargs.get('bought_at') or datetime.datetime.now().date()

        kwargs2 = {
            "buyer": buyer,
            "bought_at": bought_at,
            "count": count,
            "value": value,
            "security": security,
            "comment": kwargs.get('comment') or random_gen.gen_string(55),
            "number_segments": kwargs.get('number_segments', [])
        }
        if seller:
            kwargs2.update({"seller": seller})

        if kwargs.get('registration_type'):
            kwargs2.update(
                {'registration_type': kwargs.get('registration_type')})

        if kwargs.get('save') == False:
            return Position(**kwargs2)

        return Position.objects.create(**kwargs2)


class OptionPlanGenerator(object):

    def generate(self, **kwargs):

        company = kwargs.get('company') or CompanyGenerator().generate()

        kwargs2 = dict(
            company=company,
            board_approved_at=datetime.datetime.now().date(),
            title='some opt plan title',
            security=kwargs.get('security') or SecurityGenerator().generate(
                company=company),
            exercise_price=3,
            count=kwargs.get('count') or 3
        )

        if kwargs.get('number_segments'):
            kwargs2.update({'number_segments': kwargs.get('number_segments')})

        return OptionPlan.objects.create(**kwargs2)


class OptionTransactionGenerator(object):

    def generate(self, **kwargs):
        company = kwargs.get('company')
        if not company and kwargs.get('buyer'):
            company = kwargs.get('buyer').company
        if not company and kwargs.get('seller'):
            company = kwargs.get('seller').company
        if not company:
            company = CompanyGenerator().generate()

        buyer = kwargs.get('buyer') or ShareholderGenerator().generate(
            company=company)
        seller = kwargs.get('seller')
        count = kwargs.get('count') or 3
        kwargs.get('value') or 2
        bought_at = kwargs.get('bought_at') or datetime.datetime.now().date()

        kwargs2 = {
            "buyer": buyer,
            "bought_at": bought_at,
            "count": count,
            "option_plan": kwargs.get('option_plan') or OptionPlanGenerator(
                ).generate(company=company)
        }
        if seller:
            kwargs2.update({"seller": seller})

        if kwargs.get('number_segments'):
            kwargs2.update({'number_segments': kwargs.get('number_segments')})

        if kwargs.get('registration_type'):
            kwargs2.update(
                {'registration_type': kwargs.get('registration_type')})

        if kwargs.get('save', True):
            position = OptionTransaction.objects.create(**kwargs2)
        else:
            position = OptionTransaction(**kwargs2)

        return position


class TwoInitialSecuritiesGenerator(object):

    def generate(self, **kwargs):
        if kwargs.get('company'):
            company = kwargs.get('company')
        else:
            company = CompanyGenerator().generate()
        s1 = Security.objects.create(title='P', company=company, count=1)
        s2 = Security.objects.create(title='C', company=company, count=2)

        return (s1, s2)


class ComplexShareholderConstellationGenerator(object):

    def generate(self, **kwargs):

        company = kwargs.get('company') or CompanyGenerator().generate()
        shareholder_count = kwargs.get('shareholder_count', 10)

        # intial securities
        s1, s2 = TwoInitialSecuritiesGenerator().generate(company=company)

        # initial company shareholder
        company_shareholder_created_at = kwargs.get(
            'company_shareholder_created_at'
        ) or datetime.datetime.now()
        cs = CompanyShareholderGenerator().generate(
            company=company, security=s1,
            company_shareholder_created_at=company_shareholder_created_at)

        # random shareholder generation
        shareholders = [cs]
        # initial share seeding
        for i in range(0, shareholder_count):
            shareholders.append(PositionGenerator().generate(
                company=company, security=s1, seller=cs).buyer)

        # two shareholders sold again
        shareholders.append(
            PositionGenerator().generate(
                company=company,
                seller=shareholders[3],
                security=s1).buyer)
        shareholders.append(
            PositionGenerator().generate(
                company=company,
                seller=shareholders[6],
                security=s1).buyer)

        return shareholders, s1


class ComplexPositionsWithSegmentsGenerator(object):

    def generate(self, *args, **kwargs):
        """
        goal is to simulate for segmented shares the history of sales and buys
        of the same stocks
        """
        company = kwargs.get('company') or CompanyGenerator().generate()

        OperatorGenerator().generate(company=company)

        # intial securities
        s1, s2 = TwoInitialSecuritiesGenerator().generate(company=company)
        s1.track_numbers = True
        s1.number_segments = [u'1000-2000']
        s1.save()

        # initial company shareholder
        company_shareholder_created_at = kwargs.get(
            'company_shareholder_created_at'
        ) or datetime.datetime.now()
        cs = CompanyShareholderGenerator().generate(
            company=company, security=s1,
            company_shareholder_created_at=company_shareholder_created_at)
        s = ShareholderGenerator().generate(company=company)

        shareholders = [cs, s]
        positions = []

        # random shareholder generation
        def buy_segment(segments, buyer, seller):
            p = PositionGenerator().generate(
                company=company, security=s1, buyer=buyer,
                seller=seller, number_segments=segments)
            return p

        positions.append(buy_segment([u'1000-1050'], s, cs))
        positions.append(buy_segment([1050], cs, s))
        positions.append(buy_segment([u'1050-1100'], s, cs))
        positions.append(buy_segment([u'1101-1200', 1666], s, cs))
        positions.append(buy_segment([1050], cs, s))
        positions.append(buy_segment([1050], s, cs))

        return positions, shareholders


class MassPositionsWithSegmentsGenerator(object):

    def generate(self, *args, **kwargs):
        """
        used for performance testing. adds 100 shareholders and 1.000.000 shares
        """
        company = kwargs.get('company') or CompanyGenerator().generate()
        sh_count = 100
        segments = kwargs.get('segments', [u'1-1000000'])

        OperatorGenerator().generate(company=company)

        # intial securities
        s1, s2 = TwoInitialSecuritiesGenerator().generate(company=company)
        s1.track_numbers = True
        s1.number_segments = segments
        s1.save()

        # initial company shareholder
        company_shareholder_created_at = kwargs.get(
            'company_shareholder_created_at'
        ) or datetime.datetime.now()
        cs = CompanyShareholderGenerator().generate(
            company=company, security=s1,
            company_shareholder_created_at=company_shareholder_created_at)

        logger.info('start {} shareholder generation...'.format(sh_count))
        # shareholders
        shareholders = [ShareholderGenerator().generate(company=company) for i
                        in range(0, sh_count)]
        shareholders.append(cs)
        shareholders.reverse()

        positions = []

        def buy_segment(buyer, seller):
            logging.info('getting segment list from seller ...')
            segments = [random.choice(seller.current_segments(s1))]
            logging.info('inflating segments from seller...')
            count = len(inflate_segments(segments))

            logging.info('running position generator for position')
            p = PositionGenerator().generate(
                company=company, security=s1, buyer=buyer,
                seller=seller, number_segments=segments, count=count)
            logging.info('returning position')
            return p

        logging.info('distribute shares from cs to shareholders...')
        # spread all shares amongst shareholders
        for x in range(0, sh_count):
            if cs.share_count() > 0:
                positions.append(buy_segment(random.choice(shareholders),
                                             cs))
            else:
                logging.info('seller has no shares. skipped')

        logging.info('distribute shares amongst shareholders...')
        # shs trade amongst each other
        for x in range(0, sh_count):
            seller = random.choice(shareholders)
            if seller.share_count() > 0:
                positions.append(buy_segment(
                    random.choice(shareholders),
                    seller))

        logging.info('mass position generator finished')
        return positions, shareholders


class ComplexOptionTransactionsWithSegmentsGenerator(object):

    def generate(self, *args, **kwargs):
        """
        goal is to simulate for segmented shares the history of sales and buys
        of the same stocks
        """
        company = kwargs.get('company') or CompanyGenerator().generate()

        if not company.operator_set.exists():
            OperatorGenerator().generate(company=company)

        # intial securities
        s1, s2 = TwoInitialSecuritiesGenerator().generate(company=company)
        s1.track_numbers = True
        s1.number_segments = [u'1-3000']
        s1.save()

        # initial company shareholder
        company_shareholder_created_at = kwargs.get(
            'company_shareholder_created_at'
        ) or datetime.datetime.now()
        cs = CompanyShareholderGenerator().generate(
            company=company, security=s1,
            company_shareholder_created_at=company_shareholder_created_at)
        s = ShareholderGenerator().generate(company=company)
        optionplan = OptionPlanGenerator().generate(
            company=company, number_segments=[u'1000-2000'], security=s1)
        # initial option grant to CompanyShareholder
        ot = OptionTransactionGenerator().generate(
            company=company, security=s1, buyer=cs,
            number_segments=[u'1000-2000'], option_plan=optionplan)

        shareholders = [cs, s]
        positions = [ot]

        # random shareholder generation
        def buy_segment(segments, buyer, seller):
            p = OptionTransactionGenerator().generate(
                company=company, security=s1, buyer=buyer,
                seller=seller, number_segments=segments,
                option_plan=optionplan)
            return p

        positions.append(buy_segment([u'1000-1050'], s, cs))
        positions.append(buy_segment([1050], cs, s))
        positions.append(buy_segment([u'1050-1100'], s, cs))
        positions.append(buy_segment([u'1101-1200', 1666], s, cs))
        positions.append(buy_segment([1050], cs, s))
        positions.append(buy_segment([1050], s, cs))

        return positions, shareholders
