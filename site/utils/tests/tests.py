#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import logging

from django.core.management import call_command
from django.test import TestCase

from project.generators import CompanyGenerator
from shareholder.models import OptionTransaction
from utils.formatters import (deflate_segments, flatten_list, inflate_segments,
                              string_list_to_json)
from utils.math import substract_list
from utils.user import make_username
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


class UtilsTestCase(TestCase):

    def test_flatten_list(self):

        l = [[1, 2], [3, 4, 5], [6, 7, 8, 9, 10]]
        self.assertEqual(flatten_list(l), range(1, 11))

    def test_make_username(self):

        first_name = 'Hans Walter Peter Joao'
        last_name = 'Andreesen-Horowitz Meisen Steuer'
        email = 'thisisaverylongandnonrelevant@emailaddressforsomecompany.com'

        username = make_username(first_name, last_name, email)

        self.assertTrue(len(username) > 0)
        self.assertTrue(len(username) < 30)
        self.assertTrue(isinstance(username, str))

    def test_unique_username(self):
        """
        on prod we had
        http://sentry.ttg-dresden.de/sentry-internal/production/
        issues/28313/
        jirka2@tschitschereengreen.com
        vs
        jirka+test2@kkd-partners.com
        """
        username1 = make_username(
            'Jirka', 'Schaefer', u'jirka@tschitschereengreen.com')

        username2 = make_username(
            'Jirka2', 'Schaefer2', u'jirka2@tschitschereengreen.com')

        self.assertNotEqual(username1, username2)

    def test_string_list_to_json(self):

        with self.assertRaises(ValueError):
            string_list_to_json('[]')
            string_list_to_json('1,2,3,4--10')
            string_list_to_json('1,,2,3,4-10,11-12X')

        self.assertEqual(string_list_to_json('1,2,3,4-10'), [u'1-10'])
        self.assertEqual(string_list_to_json('1,2,3,,4-10'), [u'1-10'])
        # test removal of duplicates and that is ordered
        self.assertEqual(string_list_to_json('0, 3,,, 3, 5-10, 9-12, 2'),
                         [0, u'2-3', u'5-12'])

    def test_inflate_segments(self):
        segments = [1, 2, 3, 4, u'9-14', 18]

        res = inflate_segments(segments)

        self.assertEqual(res, [1, 2, 3, 4, 9, 10, 11, 12, 13, 14, 18])

    def test_deflate_segments(self):
        """
        watch the end of deflation logic!
        """

        # closing lonely int
        segments = [1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 14, 18]
        res = deflate_segments(segments)
        self.assertEqual(res, [u'1-4', 6, u'9-14', 18])

        # closing range
        segments = [1, 2, 3, 4, 6, 9, 10, 11, 12, 13, 14]
        res = deflate_segments(segments)
        self.assertEqual(res, [u'1-4', 6, u'9-14'])

    def test_deflate_segments_performance(self):
        """
        watch the end of deflation logic!
        """
        segments = []
        segments.extend(range(1, 1000001))
        segments.extend([1500000, 1600000])
        segments.extend(range(2000000, 8000001))
        segments.extend([9000000])
        t0 = time.clock()
        res = deflate_segments(segments)
        t1 = time.clock()
        delta = t1 - t0
        print("deflate list took {0:.4f} seconds.".format(t1 - t0))
        self.assertEqual(
            res,
            [u'1-1000000', 1500000, 1600000, u'2000000-8000000', 9000000])
        if delta > 1.1:
            logger.error(
                'BUILD performance error: test_substract_list_performance',
                extra={'delta': delta})
        self.assertLess(delta, 1.5)

    def test_substract_list_performance(self):
        """
        test performance and result
        """
        l1 = range(0, 10000000)
        l2 = range(0, 1000000)
        t0 = time.clock()
        res = substract_list(l1, l2)
        t1 = time.clock()
        delta = t1 - t0
        print("substract list took {0:.4f} seconds.".format(delta))

        self.assertEqual(res, range(1000000, 10000000))
        if delta > 0.3:
            logger.error(
                'BUILD performance error: test_substract_list_performance',
                extra={'delta': delta})
        self.assertLess(delta, 0.5)

    def test_substract_list_logic(self):
        """
        test performance and result
        """
        l1 = [5, 7, 11, 11, 11, 12, 13]
        l2 = [7, 8, 11]
        res = substract_list(l1, l2)

        self.assertEqual(res, [5, 11, 11, 12, 13])

        l1 = [5]
        l2 = [5]
        res = substract_list(l1, l2)

        self.assertEqual(res, [])
