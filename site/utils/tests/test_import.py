#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from project.generators import CompanyGenerator
from shareholder.models import OptionTransaction, Shareholder, Position
from utils.import_backends import SisWareImportBackend

logger = logging.getLogger(__name__)


class ImportTestCaseMixin(object):

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

    def test_get_or_create_user(self):
        self.backend.company = CompanyGenerator().generate()
        self.backend._get_or_create_user('1', 'first name', 'last_name',
                                         'Natürliche Person', '', '')
        user = User.objects.last()
        self.assertEqual(user.userprofile.legal_type, 'H')

        self.backend._get_or_create_user('1', 'first name', 'last_name',
                                         'Juristische Person', 'Large Corp',
                                         'Management and IT')
        user = User.objects.last()
        self.assertEqual(user.userprofile.legal_type, 'C')
        self.assertEqual(user.userprofile.company_name, 'Large Corp')
        self.assertEqual(user.userprofile.company_department, 'Management and IT')

    def test__init_import(self):

        company = CompanyGenerator().generate()
        self.backend._init_import(company.pk)
        self.assertEqual(company.security_set.count(), 0)
        self.assertEqual(company.shareholder_set.count(), 1)
        self.assertEqual(company.operator_set.count(), 1)
