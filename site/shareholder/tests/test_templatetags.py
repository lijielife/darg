#!/usr/bin/python
# -*- coding: utf-8 -*-

import mock
from dateutil.relativedelta import relativedelta
from django.test import TestCase
from django.utils import timezone

from project.generators import (OptionTransactionGenerator, PositionGenerator,
                                ShareholderGenerator)
from shareholder.templatetags.shareholder_tags import \
    get_positions_with_certificate  # noqa
from shareholder.templatetags.shareholder_tags import \
    get_total_discounted_tax_value  # noqa
from shareholder.templatetags.shareholder_tags import \
    get_vested_option_positions  # noqa:
from shareholder.templatetags.shareholder_tags import \
    shareholder_security_count  # noqa
from shareholder.templatetags.shareholder_tags import (get_vested_positions,
                                                       has_locked_shares)


class ShareholderTagsTestCase(TestCase):

    def setUp(self):
        self.shareholder = ShareholderGenerator().generate()
        self.company = self.shareholder.company
        self.position = PositionGenerator().generate(
            buyer=self.shareholder, count=30, vesting_months=24)
        self.option = OptionTransactionGenerator().generate(
            buyer=self.shareholder, count=16, vesting_months=120)

        # noise ... not to be fetched
        PositionGenerator().generate(
            buyer=self.shareholder, count=30)
        OptionTransactionGenerator().generate(
            buyer=self.shareholder, count=16)

        self.date_passed = (timezone.now() - relativedelta(years=2)).date()
        self.future_date = (timezone.now() + relativedelta(years=3)).date()

        # vesting expired
        PositionGenerator().generate(
            buyer=self.shareholder, count=30, bought_at=self.date_passed,
            vesting_months=6)
        OptionTransactionGenerator().generate(
            buyer=self.shareholder, count=16, bought_at=self.date_passed,
            vesting_months=6)

    def test_get_vested_positions(self):
        """
        return qs of positions with active vesting
        """
        self.assertEqual(
            [p for p in get_vested_positions(self.shareholder)],
            [self.position])
        self.assertEqual(
            len(get_vested_positions(self.shareholder, date=self.date_passed)),
            2)
        self.assertEqual(
            len(get_vested_positions(self.shareholder, date=self.future_date)),
            0)

    def test_get_vested_option_positions(self):
        """
        return qs of options with active vesting
        """
        self.assertEqual(
            [p for p in get_vested_option_positions(self.shareholder)],
            [self.option])
        self.assertEqual(
            len(get_vested_option_positions(self.shareholder,
                                            date=self.date_passed)),
            2)
        self.assertEqual(
            len(get_vested_option_positions(
                self.shareholder, date=self.future_date)),
            1)

    def test_get_total_discounted_tax_value(self):
        """
        return total value to be taxable
        """
        self.assertEqual(
            get_total_discounted_tax_value(self.shareholder), 3563.424)
        self.assertEqual(
            get_total_discounted_tax_value(self.shareholder,
                                           date=self.date_passed),
            4600.0)
        self.assertEqual(
            get_total_discounted_tax_value(self.shareholder,
                                           date=self.future_date),
            1064.096)

    @mock.patch('shareholder.models.Shareholder.get_positions_with_certificate')
    def test_get_positions_with_certificate(self, certificate_mock):
        """ get unsold positions with certificates """
        get_positions_with_certificate(
            self.shareholder, date=timezone.now().date(),
            security=self.company.security_set.first())
        certificate_mock.assert_called_with(
            date=timezone.now().date(),
            security=self.company.security_set.first())

    @mock.patch('shareholder.models.Shareholder.has_locked_shares')
    def test_has_locked_shares(self, locked_shares_mock):
        """ does the shareholder have locked shares """
        has_locked_shares(
            self.shareholder, date=timezone.now().date(),
            security=self.company.security_set.first())
        locked_shares_mock.assert_called_with(
            date=timezone.now().date(),
            security=self.company.security_set.first())

    @mock.patch('shareholder.models.Shareholder')
    def test_shareholder_security_count(self, shareholder_mock):
        shareholder_security_count(shareholder_mock, self.future_date)
        shareholder_mock.security_count.assert_called_with(
            date=self.future_date)
