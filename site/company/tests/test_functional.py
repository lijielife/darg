import datetime
import time

from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By

from company import page
from project.base import BaseSeleniumTestCase
from project.generators import (OperatorGenerator, PositionGenerator,
                                ShareholderGenerator,
                                TwoInitialSecuritiesGenerator, UserGenerator)
from shareholder.models import Company

User = get_user_model()


# --- FUNCTIONAL TESTS
class CompanyFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        # initial position
        shareholder = ShareholderGenerator().generate(user=self.operator.user)
        PositionGenerator().generate(
            company=self.operator.company,
            number_segments=[u'0-9999'], buyer=shareholder, count=10000)
        TwoInitialSecuritiesGenerator().generate(company=self.operator.company)

    def test_add_new_operator(self):
        """ means: create a option plan and move options for users """

        user = UserGenerator().generate()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_open_add_new_operator_form()
            p.enter_new_operator_email(user.email)
            p.click_save_new_operator()
            p.wait_until_visible(
                (By.XPATH,
                 u'//div[@id="company"]//div[contains(@class, "operators")]'
                 u'//div[contains(@class, "tr")]//div[contains(text(), "{}")]'
                 u''.format(user.email))
            )
            self.assertTrue(p.is_operator_displayed(user.email))
            self.assertTrue(user.operator_set.filter(
                company=self.operator.company).exists()
            )
        except Exception, e:
            self._handle_exception(e)

    def test_add_new_operator_invalid_user(self):
        """ means: create a option plan and move options for users """

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_open_add_new_operator_form()
            email = 'a@a.de'
            p.enter_new_operator_email(email)
            p.click_save_new_operator()
            # wait for error
            p.wait_until_visible((By.CSS_SELECTOR, '.form-error'))
            self.assertFalse(email in p.driver.page_source)
            self.assertFalse(User.objects.filter(email=email).exists())
        except Exception, e:
            self._handle_exception(e)

    def test_delete_operator(self):
        operator = OperatorGenerator().generate(
            company=self.operator.company)
        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_remove_operator(operator)
            p.wait_until_invisible(
                (By.XPATH,
                 u'//div[contains(text(), "{}")]'.format(
                     operator.user.email))
            )
            self.assertFalse(
                p.is_operator_displayed(operator.user.email)
            )
            self.assertFalse(self.operator.company.operator_set.filter(
                user=operator.user).exists())
        except Exception, e:
            self._handle_exception(e)

    def test_edit_founding_date_76(self):
        """
        edit companies founding_date using the datepicker
        """
        try:

            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("founding-date")
            p.click_open_datepicker("founding-date")
            p.click_date_in_datepicker("founding-date")
            p.save_edit("founding-date")

            # wait for form to disappear
            p.wait_until_invisible((By.CSS_SELECTOR, 'tr.founding-date form'))

            today = datetime.datetime.now().date()
            founding_date = datetime.date(today.year, today.month, 1)

            time.sleep(1)
            self.assertEqual(
                p.get_founding_date(),
                founding_date.strftime('%d.%m.%y'))

        except Exception, e:
            self._handle_exception(e)

        self.assertEqual(
            Company.objects.get(id=self.operator.company.id).founded_at,
            founding_date)

    def test_add_number_segment(self):
        """
        add number segement to existing one
        """
        for s in self.operator.company.security_set.all():
            s.track_numbers = True
            s.save()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("security")
            p.enter_string("security", "88, 99-100")
            p.save_edit("security")

            # wait for form to disappear
            p.wait_until_invisible((By.CSS_SELECTOR, 'tr.security form'))

        except Exception, e:
            self._handle_exception(e)

        self.assertTrue(
            [88, u'99-100'] in
            self.operator.company.security_set.values_list(
                'number_segments', flat=True))

    def test_alter_number_segment(self):
        """
        alter existing number segment
        """
        for security in self.operator.company.security_set.all():
            security.number_segments = [1, 2]
            security.track_numbers = True
            security.save()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("security")
            p.enter_string("security", ", 88, 99-100", clear=True)
            p.save_edit("security")

            # wait for form to disappear
            p.wait_until_invisible((By.CSS_SELECTOR, 'tr.security form'))

        except Exception, e:
            self._handle_exception(e)

        self.assertTrue(
            [88, u'99-100'] in
            self.operator.company.security_set.values_list(
                'number_segments', flat=True))

    def test_save_invalid_number_segment(self):

        for security in self.operator.company.security_set.all():
            security.number_segments = [1, 2]
            security.track_numbers = True
            security.save()

        try:
            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_to_edit("security")
            p.enter_string("security", ";X, 88, 99-100")
            p.save_edit("security")

            # wait for error
            # NOTE: this is kind of duplicate to the assertTrue below
            p.wait_until_visible((By.CSS_SELECTOR, '.editable-error'))

        except Exception, e:
            self._handle_exception(e)

        self.assertTrue(self.selenium.find_element_by_class_name(
            'editable-error').is_displayed())

    def test_no_numbered_shares(self):
        """
        test that company without numbered shares does not see anything
        """
        try:
            page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )

        except Exception, e:
            self._handle_exception(e)

        self.assertFalse(self.selenium.find_element_by_class_name(
            'numbered-segments').is_displayed())

    def test_reset_company(self):
        """
        reset company and related data and it's redirect to the new data form
        """
        try:
            user = self.operator.user

            p = page.CompanyPage(
                self.selenium,
                self.live_server_url,
                self.operator.user,
                self.operator.company
            )
            p.click_reset_company()
            p.confirm_reset_company()

            self.assertFalse(user.operator_set.exists())
            self.assertIn('/start/', p.driver.current_url)

        except Exception, e:
            self._handle_exception(e)
