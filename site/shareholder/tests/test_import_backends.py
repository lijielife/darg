#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.test import TestCase

from shareholder.import_backends import SwissBankImportBackend
from shareholder.models import Bank

CONTENT = (u"01100  0000     001008100  120160115131SNB            "
           u"Schweizerische Nationalbank                                 "
           u"Börsenstrasse 15                   Postfach 2800                      "
           u"8022      Zürich                             058 6"
           u"31 31 11                              30-5-5      "
           u"SNBZCHZZXXX   ")


class SwissBankImportBackendTestCase(TestCase):
    """
    import all swiss banks
    """
    def setUp(self):
        self.backend = SwissBankImportBackend()

    def test_call_url(self):
        response = self.backend._call_url()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Aareal', response.content)

    def test_prepare_data(self):
        class ResponseMock(object):
            def __init__(self):
                self.encoding = 'ISO-8859-2'
                self.content = CONTENT.encode(self.encoding)
        response = ResponseMock()
        data = self.backend._prepare_data(response)
        self.assertEqual(data, CONTENT)

    def test_split_line(self):
        res = self.backend._split_line(CONTENT)
        self.assertTrue(len(res.keys()), 23)
        self.assertEqual(res['address'], u'Postfach 2800')

    def test_get_or_create_bank(self):
        res = self.backend._split_line(CONTENT)
        self.backend._get_or_create_bank(res)
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(Bank.objects.first().address, u'Börsenstrasse 15')
