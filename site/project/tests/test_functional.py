#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import time

from selenium.webdriver.common.by import By

from project import page
from project.base import BaseSeleniumTestCase
from project.generators import (DEFAULT_TEST_DATA, CompanyShareholderGenerator,
                                ComplexOptionTransactionsWithSegmentsGenerator,
                                OperatorGenerator, ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator)
from shareholder.models import Security, Shareholder

from .mixins import StripeTestCaseMixin, SubscriptionTestMixin


# --- FUNCTIONAL TESTS
class StartFunctionalTestCase(StripeTestCaseMixin, SubscriptionTestMixin,
                              BaseSeleniumTestCase):

    def setUp(self):
        super(StartFunctionalTestCase, self).setUp()

        self.operator = OperatorGenerator().generate()
        TwoInitialSecuritiesGenerator().generate(company=self.operator.company)
        self.company_shareholder = CompanyShareholderGenerator().generate(
            company=self.operator.company)
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)

        # add a subscription for the company
        self.add_subscription(self.operator.company)

    def tearDown(self):
        super(StartFunctionalTestCase, self).tearDown()

        Security.objects.all().delete()

    def test_ticket_49(self):
        """ add shareholder as ops and then try login as this shareholder """
        self.operator = OperatorGenerator().generate(
            user=self.buyer.user, company=self.operator.company)

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url, self.operator.user)
            # wait for list
            start.wait_until_visible((By.CSS_SELECTOR, '#shareholder_list'))
            start.is_properly_displayed()
            self.assertEqual(start.has_shareholder_count(),
                             Shareholder.objects.count())

        except Exception, e:
            self._handle_exception(e)

    def test_ticket_8(self):
        """ adding shareholder with user and userprofile for the same user for
        many companies/registers

        means we will create 3 companies, with 3 operators and each will add the
        same shareholder for its company.

        then login as the shareholder and check what happened and what is shown
        """
        ops = []
        ops.append(OperatorGenerator().generate())
        ops.append(OperatorGenerator().generate())
        ops.append(OperatorGenerator().generate())
        for op in ops:
            CompanyShareholderGenerator().generate(company=op.company)
        user = UserGenerator().generate()

        # add subscription for companies
        [self.add_subscription(op.company) for op in ops]

        try:
            for op in ops:
                # CompanyShareholderGenerator().generate(company=op.company)
                start = page.StartPage(
                    self.selenium, self.live_server_url, op.user)
                # wait for list
                start.wait_until_visible(
                    (By.CSS_SELECTOR, u'#shareholder_list'))
                start.is_properly_displayed()
                self.assertEqual(start.has_shareholder_count(),
                                 Shareholder.objects.filter(
                                    company=op.company).count())
                self.assertEqual(user.shareholder_set.filter(
                    company=op.company).count(), 0)
                start.click_open_add_shareholder()
                start.wait_until_modal_opened('addShareholder')
                start.add_shareholder(user)
                self._screenshot()
                start.click_save_add_shareholder()
                start.is_no_errors_displayed()
                self._screenshot()
                start.close_modal('addShareholder')

                time.sleep(3)

                self.assertEqual(user.shareholder_set.filter(
                    company=op.company).count(), 1)
                # wait for list entry
                xpath = (
                    u'//div[@id="shareholder_list"]//span[text()="{}"]'
                    u''.format(user.shareholder_set.first().get_full_name()))
                start.wait_until_visible((By.XPATH, xpath))
                self.assertEqual(start.has_shareholder_count(),
                                 Shareholder.objects.filter(
                                    company=op.company).count())

            # shareholder now, no shareholder login yet
            # start = page.StartPage(
            #    self.selenium, self.live_server_url, user)
            # start.is_properly_displayed()

            self.assertEqual(user.shareholder_set.count(), 3)
            for op in ops:
                self.assertEqual(
                    user.shareholder_set.filter(company=op.company).count(), 1)

        except Exception, e:
            self._handle_exception(e)

    def test_ticket_68(self):
        """
        ensure that all share counts on start page after initial company setup
        are right
        """

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url, self.operator.user)
            # wait for list
            start.wait_until_visible((By.CSS_SELECTOR, '#shareholder_list'))
            start.is_properly_displayed()
            self.assertEqual(start.has_shareholder_count(),
                             Shareholder.objects.count())

            share_count = self.operator.company.share_count
            # company shareholder count
            self.assertEqual(int(
                start.get_row_by_shareholder(self.company_shareholder)
                .find_elements_by_tag_name('div')[-1].text),
                share_count
            )
            # totals
            self.assertEqual(
                self.selenium.find_element_by_xpath(
                    u'//div[@class="table"]/div[contains(@class, "tr")][last()]'
                    u'/div[contains(@class, "td")][last()]'
                ).text,
                "{}".format(share_count)
            )
        except Exception, e:
            self._handle_exception(e)

    def test_add_company(self):
        """
        add company with face value with decimals and large share count
        see #96
        """
        user = UserGenerator().generate()
        value = '4.5'
        count = '15000000'

        try:
            p = page.StartPage(
                self.selenium, self.live_server_url, user)
            # wait for form
            p.wait_until_visible((By.CSS_SELECTOR, '#add_company'))
            self.assertTrue(p.is_add_company_form_displayed())
            # menue is hidden
            self.assertFalse(
                self.selenium.find_element_by_css_selector('#navbar ul')
                .is_displayed())

            p.enter_add_company_data(value=value, count=count)
            p.click_save_add_company()

            # wait for form to disappear
            p.wait_until_invisible((By.CSS_SELECTOR, '#add_company'))

            self.assertEqual(p.get_form_errors(), [])
            self.assertFalse(p.is_add_company_form_displayed())
            self.assertTrue(user.operator_set.exists())
            company = user.operator_set.first().company
            self.assertEqual(DEFAULT_TEST_DATA['company_name'], company.name)
            cs = company.get_company_shareholder()
            self.assertTrue(cs.buyer.first().value, value)
            # menue is displayed
            self.assertTrue(
                self.selenium.find_element_by_css_selector('#navbar ul')
                .is_displayed())
            # captable is hidden after company add, so the user is not confused
            # and can enter a single shareholder first
            self.assertFalse(
                self.selenium.find_element_by_css_selector('#captable')
                .is_displayed())
            # but it's shown on refresh
            p.refresh()
            self.assertTrue(
                p.wait_until_visible((By.CSS_SELECTOR, '#captable'))
                .is_displayed())
            self.assertEqual(company.founded_at, datetime.date.today())

        except Exception, e:
            self._handle_exception(e)

    def test_add_shareholder_without_email(self):
        """
        add shareholder without email
        """
        op = OperatorGenerator().generate()
        self.add_subscription(op.company)
        CompanyShareholderGenerator().generate(company=op.company)
        user = UserGenerator().generate()
        user.email = None

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url, op.user)
            # wait for list
            start.wait_until_visible(
                (By.CSS_SELECTOR, '#shareholder_list'))
            start.is_properly_displayed()
            self.assertEqual(start.has_shareholder_count(),
                             Shareholder.objects.filter(
                                company=op.company).count())
            start.click_open_add_shareholder()
            start.wait_until_modal_opened('addShareholder')
            start.add_shareholder(user)
            start.click_save_add_shareholder()
            start.close_modal('addShareholder')
            time.sleep(5)
            # wait for list entry
            xpath = (
                '//div[@id="shareholder_list"]//span[text()="{}"]'
                u''.format(
                    Shareholder.objects.last().get_full_name()
                )
            )
            start.wait_until_visible((By.XPATH, xpath))
            self.assertEqual(start.has_shareholder_count(),
                             Shareholder.objects.filter(
                                company=op.company).count())
            self.assertEqual(
                user.first_name,
                Shareholder.objects.filter(
                    company=op.company).last().user.first_name)

        except Exception, e:
            self._handle_exception(e)

    def test_add_shareholder_with_existing_number(self):
        """
        add shareholder with existing number
        """
        op = OperatorGenerator().generate()
        self.add_subscription(op.company)
        user = UserGenerator().generate()
        shareholder = ShareholderGenerator().generate(company=op.company)
        user.email = None

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url, op.user)
            # wait for list
            start.wait_until_visible(
                (By.CSS_SELECTOR, '#shareholder_list'))
            start.is_properly_displayed()
            self.assertEqual(start.has_shareholder_count(),
                             Shareholder.objects.filter(
                                company=op.company).count())
            start.click_open_add_shareholder()
            start.wait_until_modal_opened('addShareholder')
            start.add_shareholder(user, number=shareholder.number)
            start.click_save_add_shareholder()
            start.close_modal('addShareholder')
            time.sleep(2)

            self.assertEqual(Shareholder.objects.filter(
                company=op.company, number=shareholder.number).count(),
                1)

        except Exception, e:
            self._handle_exception(e)

    def test_options_with_segments_display(self):
        """
        test on start page that options with segments are show properly
        """
        optiontransactions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()

        # add a subscription for the company
        self.add_subscription(shs[0].company)

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url,
                shs[0].company.operator_set.first().user)
            # wait for list
            start.wait_until_visible((By.CSS_SELECTOR, '#shareholder_list'))
            start.is_properly_displayed()
            time.sleep(3)
            for shareholder in shs[1:]:  # not for company shareholder
                # FIXME
                row_xpath = (
                    # '//div[contains(@class, "options")]/div[./div/span="{}"
                    # and contains(@class, "tr")]'.format(
                    #    shareholder.get_full_name()))
                    '//div[contains(@class, "options")]/'
                    'div[contains(@class, "tr")]')
                row = self.selenium.find_elements_by_xpath(row_xpath)[0]
                self.assertEqual(row.find_element_by_class_name('number').text,
                                 shareholder.number)
                self.assertEqual(row.find_element_by_class_name('share').text,
                                 u'6 (6.00%)')
                self.assertEqual(
                    row.find_element_by_class_name('full-name').text,
                    shareholder.get_full_name())

        except Exception, e:
            self._handle_exception(e)

    def test_general_display(self):
        """
        test on start page that diverse things are shown properly
        e.g. #128
        """
        optiontransactions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()

        # add a subscription for the company
        self.add_subscription(shs[0].company)

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url,
                shs[0].company.operator_set.first().user)
            # wait for list
            start.wait_until_visible((By.CSS_SELECTOR, '#shareholder_list'))
            start.is_properly_displayed()
            # self.assertEqual(start.get_total_share_count(), 3)
            self.assertEqual(start.get_company_share_count(), 100)
            self.assertEqual(start.get_total_share_count(),
                             start.get_company_share_count())

        except Exception, e:
            self._handle_exception(e)

    def test_table_actions(self):
        """
        test on start page that diverse things are shown properly
        e.g. #128
        """
        optiontransactions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        for x in range(0, 30):
            ShareholderGenerator().generate(company=shs[0].company)

        # add a subscription for the company
        self.add_subscription(shs[0].company)

        try:
            start = page.StartPage(
                self.selenium, self.live_server_url,
                shs[0].company.operator_set.first().user)
            # wait for list
            start.wait_until_visible((By.CSS_SELECTOR, '#shareholder_list'))

            # search
            start.is_properly_displayed()
            # FIXME doing strang things here
            start.enter_search_term(shs[0].user.last_name)
            time.sleep(1)
            start.click_search()
            start.refresh()
            time.sleep(2)
            start.enter_search_term(shs[0].user.last_name)
            time.sleep(1)
            start.click_search()
            time.sleep(1)
            self.assertEqual(start.has_shareholder_count(), 1)

            # paginate
            start.refresh()
            start.is_properly_displayed()
            self.assertEqual(start.has_shareholder_count(), 20)
            start.click_paginate_next()
            time.sleep(1)
            self.assertEqual(start.has_shareholder_count(), 12)

            # sort
            start.refresh()
            start.is_properly_displayed()
            start.sort_table_by_number()
            time.sleep(2)
            numbers = start.driver.find_elements_by_class_name('number')
            prev = None
            for number in numbers:
                if prev is None:
                    prev = number.text
                    continue
                self.assertTrue(prev < number.text)

        except Exception, e:
            self._handle_exception(e)

    def test_operator_same_email_as_shareholder(self):
        """
        user signs up and adds himself as shareholder
        """

        try:
            self.assertEqual(
                self.operator.user.shareholder_set.filter(
                    company=self.operator.company
                ).count(), 0)

            start = page.StartPage(
                self.selenium, self.live_server_url, self.operator.user)
            # wait for list
            start.wait_until_visible((By.CSS_SELECTOR, '#shareholder_list'))
            start.is_properly_displayed()
            start.click_open_add_shareholder()
            start.wait_until_modal_opened('addShareholder')
            start.add_shareholder(self.operator.user)
            start.click_save_add_shareholder()
            start.is_no_errors_displayed()
            start.close_modal('addShareholder')
            time.sleep(5)
            # wait for list entry
            xpath = (
                u'//div[@id="shareholder_list"]//div/span[text()="{}"]'.format(
                    self.operator.user.shareholder_set.first().get_full_name())
            )
            start.wait_until_visible((By.XPATH, xpath))
            self.assertEqual(start.has_shareholder_count(),
                             Shareholder.objects.filter(
                                company=self.operator.company).count())

            self.assertEqual(
                self.operator.user.shareholder_set.filter(
                    company=self.operator.company
                ).count(), 1)

        except Exception, e:
            self._handle_exception(e)
