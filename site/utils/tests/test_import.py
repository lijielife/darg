#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import logging

from dateutil.parser import parse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase

from project.generators import CompanyGenerator, ShareholderGenerator
from shareholder.models import OptionTransaction, Position, Shareholder
from utils.import_backends import SisWareImportBackend, SECURITIES

logger = logging.getLogger(__name__)


class ImportTestCaseMixin(object):
    fixtures = ['initial.json']

    def setUp(self):
        self.filename = 'utils/tests/csv/sisware_export.csv'
        self.code = 'rot13'
        self.company = CompanyGenerator().generate()
        self.backend = SisWareImportBackend(self.filename)

    def assertImport(self):
        """
        reusable asserts after an import
        """
        # trigger fully featured share register validation,
        # raises ValidationError
        self.company.refresh_from_db()  # always use latest data
        with self.assertRaises(ValidationError):
            self.company.full_validate()


class CommandTestCase(ImportTestCaseMixin, TestCase):

    def test_import_initial(self):
        call_command('import', str(self.company.pk), self.filename)
        self.assertImport()


class SisWareImportBackendTestCase(ImportTestCaseMixin, TestCase):

    def test_encoding(self):
        """
        file content must be encoded to utf8 for db insertion
        """
        with open(self.filename) as fp:
            for i, line in enumerate(fp):
                if i == 18:
                    res = self.backend.to_unicode(line)

        self.assertIn(u'Natürliche', res)

    def test_import_repeated(self):

        self.backend.import_from_file(str(self.company.pk))
        self.assertImport()

        # does the company be a seller for each position?
        self.company_shareholder = self.company.get_company_shareholder()
        self.assertEqual(self.backend.row_count,
                         self.company_shareholder.seller.count() +
                         OptionTransaction.objects.filter(
                            option_plan__company=self.company).exclude(
                            seller__isnull=True
                         ).count() -
                         self.company.get_dispo_shareholder().buyer.count() +
                         1  # deleted but previously imported
                         )

        # redo the import and validate again
        self.backend.import_from_file(str(self.company.pk))
        self.assertImport()

        # does the company be a seller for each position?
        self.company_shareholder = self.company.get_company_shareholder()
        self.assertEqual(self.backend.row_count,
                         self.company_shareholder.seller.count() +
                         OptionTransaction.objects.filter(
                            option_plan__company=self.company).exclude(
                            seller__isnull=True
                         ).count() -
                         self.company.get_dispo_shareholder().buyer.count() +
                         1  # deleted but previously imported
                         )
        self.assertEqual(self.company_shareholder.number, u'1913')

        # legal_type import cross check
        content = '\n'.join(self.backend.file_content)
        count = content.count('Jurist')
        self.assertEqual(User.objects.filter(
            userprofile__legal_type='C').count(), count + 1)  # + dispo sh

        # check shareholder #
        for line in self.backend.file_content:
            self.assertEqual(
                Shareholder.objects.filter(number=line.split(',')[0]).count(),
                1)

        # check registration type
        self.assertEqual(
            Position.objects.filter(registration_type='1').count(), 3)
        self.assertEqual(
            Position.objects.filter(registration_type='2').count(),
            self.backend.row_count - OptionTransaction.objects.filter(
                option_plan__company=self.company).exclude(
                    seller__isnull=True
                ).count() - 1
            )

        # option plan
        self.assertEqual(self.company.optionplan_set.count(), 3)
        self.assertEqual(self.company.security_set.count(), 3)

        # maling_type
        self.assertEqual(
            self.company.shareholder_set.filter(
                mailing_type__isnull=True).exists(), False)
        self.assertEqual(
            self.company.shareholder_set.filter(mailing_type='0').count(),
            1 + 1)  # + 1 dispo sh

        # cuspip
        self.assertEqual(
            self.company.security_set.filter(
                cusip__isnull=True).exists(), 0)  # corp sh
        # each of the 3 securities should have the same cusip due to our test
        # data
        self.assertEqual(
            self.company.security_set.filter(cusip='22570493').count(), 3)

        # positions
        self.assertEqual(
            Position.objects.filter(depot_type__isnull=True).count(), 0)
        #  3 regular + 3 dispo sh
        self.assertEqual(Position.objects.filter(depot_type='1').count(), 6)
        self.assertEqual(Position.objects.filter(depot_type='2').count(), 0)
        self.assertEqual(Position.objects.filter(depot_type='0').count(), 11)
        self.assertEqual(
            Position.objects.filter(stock_book_id__isnull=True).count(), 0)

        # options
        self.assertEqual(
            OptionTransaction.objects.filter(depot_type='1').count(), 1)
        self.assertEqual(
            OptionTransaction.objects.filter(depot_type='2').count(), 0)
        self.assertEqual(
            OptionTransaction.objects.filter(depot_type='0').count(), 9)
        self.assertEqual(OptionTransaction.objects.filter(
            depot_type__isnull=True).count(), 0)
        self.assertEqual(OptionTransaction.objects.filter(
            stock_book_id__isnull=True).count(), 3)
        self.assertEqual(OptionTransaction.objects.filter(
            certificate_id__isnull=True).count(), 3)
        self.assertEqual(OptionTransaction.objects.filter(
            seller__isnull=True).count(), 3)
        for security in self.company.security_set.all():
            self.assertEqual(self.company_shareholder.options_count(
                security=security), 0)

        # share counts
        self.assertEqual(self.company.share_count, 17439)
        for sec in self.company.security_set.all():
            self.assertEqual(
                sec.count,
                SECURITIES[str(sec.face_value).split('.')[0]])

    def test_get_or_create_user(self):
        self.backend.company = CompanyGenerator().generate()
        kwargs = dict(shareholder_id='1', first_name='first name',
                      last_name='last_name', legal_type='Natürliche Person',
                      company='',
                      department='', title='Prof.',
                      salutation='Herr', street='Oxford St.',
                      street2='c/o Hamster',
                      pobox='PO123456', postal_code='X3a',
                      city='London', country='England',
                      language='Afghan Sign Language',
                      birthday='1943-03-06 00:00:00.000',
                      c_o='Walter Kalter', nationality='England'
                      )
        self.backend._get_or_create_user(**kwargs)
        user = User.objects.last()
        for k, v in kwargs.iteritems():
            if hasattr(user, k):
                self.assertEqual(getattr(user, k), v)
            elif hasattr(user.userprofile, k):
                if k in ['country', 'nationality']:
                    self.assertEqual(
                        getattr(user.userprofile, k).name, 'United Kingdom')
                elif k == 'language':
                    self.assertEqual(
                        getattr(user.userprofile, k), 'afg')
                elif k == 'legal_type':
                    self.assertEqual(getattr(user.userprofile, k), 'H')
                elif k == 'birthday':
                    self.assertEqual(getattr(user.userprofile, k),
                                     parse(v).date())
                else:
                    self.assertEqual(getattr(user.userprofile, k), v)
            elif hasattr(user.shareholder_set.first(), k):
                self.assertEqual(user.shareholder_set.first().number, v)

        kwargs.update({'legal_type': 'Juristische Person',
                       'company': 'Large Corp',
                       'department': 'Management and IT'
                       })
        self.backend._get_or_create_user(**kwargs)

        user = User.objects.last()
        self.assertEqual(user.userprofile.legal_type, 'C')
        self.assertEqual(user.userprofile.company_name, 'Large Corp')
        self.assertEqual(user.userprofile.company_department,
                         'Management and IT')

    def test_get_or_update_init_date(self):

        ShareholderGenerator().generate(company=self.company, number='1913')
        ShareholderGenerator().generate(company=self.company, number='1157')
        sx = ShareholderGenerator().generate(
            company=self.company, number='1914')
        profile = sx.user.userprofile
        profile.initial_registration_at = None
        profile.save()

        self.backend.company = self.company
        self.backend._get_or_update_init_date()
        self.assertEqual(list(Shareholder.objects.filter(
            company=self.backend.company,
            user__userprofile__initial_registration_at__isnull=False
            ).values_list(
                'user__userprofile__initial_registration_at', flat=True
            )),
            [datetime.datetime.now().date(), datetime.datetime.now().date()]
        )

    def test__init_import(self):

        self.backend._init_import(self.company.pk)
        self.assertEqual(self.company.security_set.count(), 3)
        self.assertEqual(self.company.shareholder_set.count(), 1)
        self.assertEqual(self.company.operator_set.count(), 1)
