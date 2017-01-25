#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal

from django.test import TestCase

from project.generators import (
    CompanyGenerator, ShareholderGenerator, PositionGenerator,
    SecurityGenerator)

from shareholder.models import Shareholder


class CompanyModelTestCase(TestCase):

    def _prepare_split_scenario(self):
        company = CompanyGenerator().generate()
        security = SecurityGenerator().generate(company=company)
        cshareholder = ShareholderGenerator().generate(company=company)
        shareholder1 = ShareholderGenerator().generate(company=company)
        shareholder2 = ShareholderGenerator().generate(company=company)
        shareholder3 = ShareholderGenerator().generate(company=company)
        shareholder4 = ShareholderGenerator().generate(company=company)
        PositionGenerator().generate(
            buyer=cshareholder, count=10000, value=1000, security=security,
            seller=None)
        p1 = PositionGenerator().generate(
            buyer=shareholder1, count=100, value=20, seller=cshareholder,
            security=security)
        p2 = PositionGenerator().generate(
            buyer=shareholder2, count=200, value=40, seller=cshareholder,
            security=security)
        p3 = PositionGenerator().generate(
            buyer=shareholder3, count=900, value=60, seller=cshareholder,
            security=security)
        p4 = PositionGenerator().generate(
            buyer=cshareholder, count=600, value=80, seller=shareholder3,
            security=security)
        PositionGenerator().generate(
            buyer=cshareholder, count=1000, value=1000, security=security,
            seller=None)
        company.share_count = 11000
        company.save()

        return dict(
            company=company, cshareholder=cshareholder,
            shareholder1=shareholder1, shareholder2=shareholder2,
            shareholder3=shareholder3, shareholder4=shareholder4,
            p1=p1, p2=p2, p3=p3, p4=p4, security=security)

    def test_split_shares(self):
        """ test that split shares truely works

            we will use the maximum crazy scenario for that

            initial
            -------
            company: 10000 shares a 1000 eur nominal
            shareholder1: 100 shares a 20 price
            shareholder2: 200 shares a 40 price
            shareholder3: 300 shares a 60 price
            shareholder3: sold 600 shares previously
            company increased capital before by another 1000 shares

            after 1:100
            ----
            all % should stay equal
            overall capital should stay equal
            share count should have * 100

            we will use maximum if FE-close logic to check the data
            shown to the user
        """
        # prepare data
        objs = self._prepare_split_scenario()
        security = objs['security']
        company = objs['company']
        shareholder1 = objs['shareholder1']
        shareholder2 = objs['shareholder2']
        shareholder3 = objs['shareholder3']
        cshareholder = objs['cshareholder']

        self.assertEqual(company.share_count, 11000)
        self.assertEqual(company.get_total_capital(), Decimal(1100000))

        # exec
        company.split_shares(data=dict(
            dividend=1, divisor=100, security=security,
            execute_at=datetime.datetime.now()))

        # asserts
        self.assertEqual(
            Shareholder.objects.get(id=shareholder1.id).share_count(), 10000)
        self.assertEqual(
            Shareholder.objects.get(id=shareholder2.id).share_count(), 20000)
        self.assertEqual(
            Shareholder.objects.get(id=shareholder3.id).share_count(), 30000)
        self.assertEqual(
            Shareholder.objects.get(id=cshareholder.id).share_count(), 1040000)
        self.assertEqual(company.share_count, 1100000)
        self.assertEqual(float(company.get_total_capital()), float(110000000))

    def test_split_split_shares(self):
        """ split, and split once more. will it work?
        """

        # prepare data
        objs = self._prepare_split_scenario()
        security = objs['security']
        company = objs['company']
        shareholder1 = objs['shareholder1']
        shareholder2 = objs['shareholder2']
        shareholder3 = objs['shareholder3']
        cshareholder = objs['cshareholder']

        self.assertEqual(company.share_count, 11000)

        # exec
        company.split_shares(data=dict(
            dividend=1, divisor=100, security=security,
            execute_at=datetime.datetime.now()))

        # exec
        company.split_shares(data=dict(
            dividend=1, divisor=100, security=security,
            execute_at=datetime.datetime.now()))

        # asserts
        self.assertEqual(
            Shareholder.objects.get(id=shareholder1.id).share_count(), 1000000)
        self.assertEqual(
            Shareholder.objects.get(id=shareholder2.id).share_count(), 2000000)
        self.assertEqual(
            Shareholder.objects.get(id=shareholder3.id).share_count(), 3000000)
        self.assertEqual(
            Shareholder.objects.get(id=cshareholder.id).share_count(),
            104000000)
        self.assertEqual(company.share_count, 110000000)
