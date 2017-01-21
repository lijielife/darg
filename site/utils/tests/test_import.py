#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from dateutil.parser import parse
from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from project.generators import CompanyGenerator
from shareholder.models import OptionTransaction, Position, Shareholder
from utils.import_backends import SisWareImportBackend

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
                            option_plan__company=self.company).count()
                         )

        # redo the import and validate again
        self.backend.import_from_file(str(self.company.pk))
        self.assertImport()

        # does the company be a seller for each position?
        self.company_shareholder = self.company.get_company_shareholder()
        self.assertEqual(self.backend.row_count,
                         self.company_shareholder.seller.count() +
                         OptionTransaction.objects.filter(
                            option_plan__company=self.company).count()
                         )
        self.assertEqual(self.company_shareholder.number, u'1913')

        # legal_type import cross check
        content = '\n'.join(self.backend.file_content)
        count = content.count('Jurist')
        self.assertEqual(User.objects.filter(
            userprofile__legal_type='C').count(), count)

        # check shareholder #
        for line in self.backend.file_content:
            self.assertEqual(
                Shareholder.objects.filter(number=line.split(',')[0]).count(),
                1)

        # check registration type
        self.assertEqual(
            Position.objects.filter(registration_type='1').count(), 1)
        self.assertEqual(
            Position.objects.filter(registration_type='2').count(),
            self.backend.row_count - OptionTransaction.objects.filter(
                option_plan__company=self.company).count() - 1
            )

        # option plan
        self.assertEqual(self.company.optionplan_set.count(), 3)
        self.assertEqual(self.company.security_set.count(), 3)

        # maling_type
        self.assertEqual(
            self.company.shareholder_set.filter(
                mailing_type__isnull=True).exists(), False)
        self.assertEqual(
            self.company.shareholder_set.filter(mailing_type='0').count(), 1)

        # cuspip
        self.assertEqual(
            self.company.security_set.filter(
                cusip__isnull=True).exists(), 0)  # corp sh
        # each of the 3 securities should have the same cusip due to our test
        # data
        self.assertEqual(
            self.company.security_set.filter(cusip='22570493').count(), 3)

        # options
        self.assertEqual(
            Position.objects.filter(depot_type__isnull=True).count(), 0)
        self.assertEqual(Position.objects.filter(depot_type='1').count(), 0)
        self.assertEqual(Position.objects.filter(depot_type='2').count(), 1)
        self.assertEqual(Position.objects.filter(depot_type='0').count(), 11)
        self.assertEqual(
            Position.objects.filter(stock_book_id__isnull=True).count(), 0)

        # positions
        self.assertEqual(
            OptionTransaction.objects.filter(depot_type='1').count(), 1)
        self.assertEqual(
            OptionTransaction.objects.filter(depot_type='2').count(), 0)
        self.assertEqual(
            OptionTransaction.objects.filter(depot_type='0').count(), 6)
        self.assertEqual(OptionTransaction.objects.filter(
            depot_type__isnull=True).count(), 0)
        self.assertEqual(OptionTransaction.objects.filter(
            stock_book_id__isnull=True).count(), 0)
        self.assertEqual(OptionTransaction.objects.filter(
            certificate_id__isnull=True).count(), 0)

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

    def test__init_import(self):

        company = CompanyGenerator().generate()
        self.backend._init_import(company.pk)
        self.assertEqual(company.security_set.count(), 0)
        self.assertEqual(company.shareholder_set.count(), 1)
        self.assertEqual(company.operator_set.count(), 1)
