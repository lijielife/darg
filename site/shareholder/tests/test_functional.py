# -*- coding: utf-8 -*-

import datetime
import time
import unittest
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from selenium.webdriver.common.by import By

from project.base import BaseSeleniumTestCase
from project.generators import (CompanyShareholderGenerator,
                                ComplexOptionTransactionsWithSegmentsGenerator,
                                ComplexPositionsWithSegmentsGenerator,
                                OperatorGenerator, OptionPlanGenerator,
                                OptionTransactionGenerator, PositionGenerator,
                                ShareholderGenerator,
                                TwoInitialSecuritiesGenerator)
from shareholder import page
from shareholder.models import (OptionPlan, OptionTransaction, Position,
                                Security, Shareholder)


# --- FUNCTIONAL TESTS
class ShareholderDetailFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)
        self.cs = CompanyShareholderGenerator().generate(
            company=self.operator.company)
        PositionGenerator().generate(
            buyer=self.buyer, seller=self.cs, count=3,
            security=self.operator.company.security_set.first())

    def tearDown(self):
        Security.objects.all().delete()

    def test_display(self):
        """
        test if all data is shown properly
        """
        try:

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': self.buyer.id}
                    )
                )
            # wait for 'link'
            p.wait_until_visible(
                (By.CSS_SELECTOR, 'div.shareholder-number span.el-icon-pencil'))
            time.sleep(1)
            self.assertIn(
                self.buyer.user.userprofile.get_legal_type_display(),
                p.get_field('legal-type'))

            profile = self.buyer.user.userprofile
            profile.initial_registration_at = datetime.date(2013, 1, 13)
            profile.legal_type = 'C'
            profile.save()
            p.refresh()
            p.wait_until_visible(
                (By.CSS_SELECTOR, 'div.shareholder-number span.el-icon-pencil'))
            time.sleep(3)
            self.assertIn(profile.get_legal_type_display(),
                          p.get_field('legal-type'))
            self.assertIn(profile.initial_registration_at.strftime('%-d.%m.%y'),
                          p.get_field('initial_registration_at'))
            self.assertIn(str(float(self.buyer.cumulated_face_value())),
                          p.get_field('cumulated-face-value'))

        except Exception, e:
            self._handle_exception(e)

    def test_edit_shareholder_number_53(self):
        """ means: create a option plan and move options for users """
        try:

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': self.buyer.id}
                    )
                )
            # wait for 'link'
            p.wait_until_visible(
                (By.CSS_SELECTOR, 'div.shareholder-number span.el-icon-pencil'))
            p.click_to_edit("shareholder-number")
            p.edit_field(99, "shareholder-number")
            p.save_edit("shareholder-number")
            # wait for form to disappear
            p.wait_until_invisible(
                (By.CSS_SELECTOR, 'div.shareholder-number form'))

        except Exception, e:
            self._handle_exception(e)

        shareholder = Shareholder.objects.get(id=self.buyer.id)
        self.assertEqual(shareholder.number, str(99))

    def test_edit_company_department(self):
        """
        edit company department
        """
        profile = self.buyer.user.userprofile
        profile.legal_type = 'C'
        profile.save()

        try:

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': self.buyer.id}
                    )
                )
            # wait for 'link'
            p.wait_until_visible(
                (By.CSS_SELECTOR, 'div.company-department span.el-icon-pencil'))
            p.click_to_edit("company-department")
            p.edit_field('IT Security Dep.', "company-department")
            p.save_edit("company-department")
            # wait for form to disappear
            p.wait_until_invisible(
                (By.CSS_SELECTOR, 'div.company-department form'))

        except Exception, e:
            self._handle_exception(e)

        shareholder = Shareholder.objects.get(id=self.buyer.id)
        self.assertEqual(shareholder.user.userprofile.company_department,
                         'IT Security Dep.')

    def test_edit_legal_type(self):
        """ means: create a option plan and move options for users """
        try:

            self.assertEqual(self.buyer.user.userprofile.legal_type, 'H')

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': self.buyer.id}
                    )
                )
            # wait for 'link'
            p.wait_until_visible(
                (By.CSS_SELECTOR, '.legal-type span.el-icon-pencil'))
            p.click_to_edit("legal-type")
            p.select_type("legal-type", _('Corporate'))
            p.save_edit("legal-type")
            p.wait_until_js_rendered()
            time.sleep(2)

            profile = self.buyer.user.userprofile
            profile.refresh_from_db()
            self.assertEqual(profile.legal_type, 'C')

        except Exception, e:
            self._handle_exception(e)

    def test_edit_mailing_type(self):
        """ edit mailing type for user """
        try:

            self.assertEqual(self.buyer.mailing_type, 1)

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': self.buyer.id}
                    )
                )
            # wait for 'link'
            p.wait_until_visible(
                (By.CSS_SELECTOR, '.mailing-type span.el-icon-pencil'))
            p.click_to_edit("mailing-type")
            p.select_type("mailing-type", _('via Email'))
            p.save_edit("mailing-type")
            # wait for form to disappear
            p.wait_until_invisible(
                (By.CSS_SELECTOR, '.mailing-type form'))

            self.buyer.refresh_from_db()
            self.assertEqual(self.buyer.mailing_type, '2')

        except Exception, e:
            self._handle_exception(e)

    def test_edit_birthday_76(self):
        """
        edit shareholders birthday using the datepicker
        """
        try:
            today = datetime.datetime.now().date()
            birthday = datetime.date(today.year, today.month, today.day)

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': self.buyer.id}
                    )
                )
            # wait for 'link'
            p.wait_until_visible(
                (By.CSS_SELECTOR, 'div.birthday span.el-icon-pencil'))
            p.click_to_edit("birthday")
            p.click_open_datepicker("birthday")
            p.click_date_in_datepicker("birthday", birthday)
            p.save_edit("birthday")
            # wait for form to disappear
            p.wait_until_invisible((By.CSS_SELECTOR, 'div.birthday form'))

            self.assertEqual(
                p.get_birthday(),
                birthday.strftime('%d.%m.%y'))

        except Exception, e:
            self._handle_exception(e)

        shareholder = Shareholder.objects.get(id=self.buyer.id)
        self.assertEqual(
            shareholder.user.userprofile.birthday, birthday)

    def test_shareholder_detail_with_mixed_segments(self):
        """
        test that security with and without segments is properly displayed
        """
        positions, shs = ComplexPositionsWithSegmentsGenerator().generate(
            company=self.operator.company)

        try:

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': shs[1].pk}
                    )
                )
            # wait for table
            p.wait_until_visible((By.CSS_SELECTOR,
                                  'div.table.stock div.tr.security'))
            self.assertEqual(p.get_securities(),
                             [u'0', u'', u'6', u'1000-1200, 1666'])

        except Exception, e:
            self._handle_exception(e)

    def test_change_email_to_operator(self):
        """
        operator changes other shareholders email to his own ones. make sure he
        cannot have two users with the same email
        """
        try:

            p = page.ShareholderDetailPage(
                self.selenium, self.live_server_url, self.operator.user,
                path=reverse(
                    'shareholder',
                    kwargs={'pk': self.buyer.id}
                    )
                )
            # wait for 'link'
            p.wait_until_visible(
                (By.CSS_SELECTOR, 'div.user-email span.el-icon-pencil'))
            p.wait_until_js_rendered()  # prevent Element is not clickable ...
            p.click_to_edit("user-email")
            p.edit_field(self.operator.user.email, "user-email")
            p.save_edit("user-email")
            # wait for form to disappear
            p.wait_until_invisible((By.CSS_SELECTOR, 'div.user-email form'))

            self.assertEqual(
                User.objects.filter(email=self.operator.user.email).count(),
                1)
            self.assertTrue(self.selenium.find_element_by_class_name(
                'form-error').is_displayed())
            self.assertIn(
                _('This email is already taken by another user/shareholder.'),
                self.selenium.page_source)

        except Exception, e:
            self._handle_exception(e)


class PositionDetailFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        self.poss, self.shs = ComplexPositionsWithSegmentsGenerator().generate(
            company=self.operator.company)
        self. position = self.poss[-1]
        self.position.certificate_id = '8888'
        self.position.save()
        self.page = page.PositionDetailPage(
            self.selenium, self.live_server_url, self.operator.user,
            path=reverse('position', kwargs={'pk': self.position.pk}))

    def test_display(self):
        """
        test if all data is shown properly
        """
        try:

            # wait for angular load
            time.sleep(1)
            self.assertIn(
                self.position.get_depot_type_display(),
                self.page.get_field('depot-type'))
            self.assertIn(
                self.position.stock_book_id,
                self.page.get_field('stock-book-id'))
            self.assertIn(
                self.position.certificate_id,
                self.page.get_field('certificate-id'))

        except Exception, e:
            self._handle_exception(e)

    def test_links(self):
        """
        test if all data is shown properly
        """
        try:

            # wait for angular load
            time.sleep(1)
            self.assertIn(
                reverse('shareholder', kwargs={'pk': self.position.seller.pk}),
                self.page.get_url('seller'))
            self.assertIn(
                reverse('shareholder', kwargs={'pk': self.position.buyer.pk}),
                self.page.get_url('buyer'))

        except Exception, e:
            self._handle_exception(e)


class OptionTransactionDetailFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        self.poss, self.shs = ComplexOptionTransactionsWithSegmentsGenerator() \
            .generate(company=self.operator.company)
        self.optiontransaction = self.poss[-1]
        self.page = page.OptionTransactionDetailPage(
            self.selenium, self.live_server_url, self.operator.user,
            path=reverse('optiontransaction',
                         kwargs={'pk': self.optiontransaction.pk}))

    def test_display(self):
        """
        test if all data is shown properly
        """
        try:

            # wait for angular load
            time.sleep(1)
            self.assertIn(
                self.optiontransaction.get_depot_type_display(),
                self.page.get_field('depot-type'))
            self.assertIn(
                self.optiontransaction.stock_book_id,
                self.page.get_field('stock-book-id'))
            self.assertIn(
                self.optiontransaction.bought_at.strftime('%-d.%m.%y'),
                self.page.get_field('bought-at')
            )
            self.assertIn(
                self.optiontransaction.certificate_id,
                self.page.get_field('certificate-id'))

        except Exception, e:
            self._handle_exception(e)

    def test_links(self):
        """
        test if all data is shown properly
        """
        try:

            # wait for angular load
            time.sleep(1)
            self.assertIn(
                reverse('shareholder',
                        kwargs={'pk': self.optiontransaction.seller.pk}),
                self.page.get_url('seller'))
            self.assertIn(
                reverse('shareholder',
                        kwargs={'pk': self.optiontransaction.buyer.pk}),
                self.page.get_url('buyer'))
            self.assertIn(
                reverse(
                    'optionplan',
                    kwargs={
                        'optionsplan_id': self.optiontransaction.option_plan.pk
                    }),
                self.page.get_url('option-plan'))

        except Exception, e:
            self._handle_exception(e)


class OptionsFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        self.securities = TwoInitialSecuritiesGenerator().generate(
            company=self.operator.company)
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)

    def tearDown(self):
        Security.objects.all().delete()

    def test_add_optionplan_96(self):
        """
        test add option plan with large numbers and floating point price
        """
        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')

            self.assertTrue(app.is_option_plan_form_open())

            app.enter_option_plan_form_data(count=15000000, exercise_price=4.55)
            app.click_save_option_plan_form()

            # wait for form to disappear
            app.close_modal('addOptionPlan')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))

            self.assertTrue(app.is_no_errors_displayed())

            op = OptionPlan.objects.latest('pk')
            self.assertEqual(op.exercise_price, Decimal('4.55'))
            self.assertEqual(op.count, 15000000)

        except Exception, e:
            self._handle_exception(e)

    def test_base_use_case(self):
        """ means: create a option plan and move options for users """

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')

            self.assertTrue(app.is_option_plan_form_open())

            app.enter_option_plan_form_data()
            app.click_save_option_plan_form()

            # wait for form to disappear
            app.close_modal('addOptionPlan')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))

            self.assertTrue(app.is_no_errors_displayed())

            app.click_open_transfer_option()
            app.enter_transfer_option_data(
                seller=self.buyer, buyer=self.seller,
                count=self.buyer.options_count())
            app.click_save_transfer_option()

            # wait for form to disappear
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))

            ot = self.buyer.option_buyer.last()
            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_shown(
                buyer=self.buyer, seller=self.seller
            ))
            self.assertTrue(app.is_option_date_equal('13.05.16'))
            self.assertTrue(app.is_option_plan_displayed(
                ot.option_plan.security))
            self.assertTrue(app.is_shareholder_name_displayed(self.seller))
            self.assertTrue(app.is_shareholder_name_displayed(self.buyer))

        except Exception, e:
            self._handle_exception(e)

    def test_base_use_case_with_optional_fields(self):
        """ means: create a option plan and move options for users """

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')
            app.enter_option_plan_form_data()
            app.click_save_option_plan_form()

            # wait for form to disappear
            app.close_modal('addOptionPlan')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))

            app.click_open_transfer_option()
            app.show_optional_fields()
            app.enter_transfer_option_data(
                seller=self.buyer, buyer=self.seller, certificate_id='33',
                stock_book_id='44', depot_type='1',
                count=self.buyer.options_count())
            app.click_save_transfer_option()

            # wait for form to disappear
            app.close_modal('addOptionTransaction')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_shown(
                seller=self.buyer, buyer=self.seller,
                count=self.buyer.options_count()
            ))
            self.assertTrue(app.is_option_date_equal('13.05.16'))
            security = self.buyer.option_buyer.first().option_plan.security
            self.assertTrue(app.is_option_plan_displayed(security))
            optiontransaction = OptionTransaction.objects.last()
            self.assertEqual(optiontransaction.certificate_id, '33')
            self.assertEqual(optiontransaction.stock_book_id, '44')
            self.assertEqual(optiontransaction.depot_type, '1')

        except Exception, e:
            self._handle_exception(e)

    def test_base_use_case_no_buyer(self):
        """ test that options transfer form is working properly
        if there is no buyer selected """

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.prepare_optionplan_fixtures()

            self.assertTrue(app.is_option_plan_displayed(
                OptionPlan.objects.last().security))

            app.click_open_transfer_option()
            app.enter_transfer_option_data(seller=self.seller)
            app.click_save_transfer_option()

            # wait for error
            app.wait_until_visible((By.CSS_SELECTOR, '.form-error'))

            self.assertFalse(app.is_no_errors_displayed())
        except Exception, e:
            self._handle_exception(e)

    def test_base_use_case_no_seller(self):
        """ test that options transfer form is working properly
        if there is no seller selected """

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.prepare_optionplan_fixtures()

            self.assertTrue(app.is_option_plan_displayed(
                OptionPlan.objects.last().security))

            app.click_open_transfer_option()
            app.enter_transfer_option_data(buyer=self.buyer)
            app.click_save_transfer_option()

            # wait for error
            app.wait_until_visible((By.CSS_SELECTOR, '.form-error'))

            self.assertFalse(app.is_no_errors_displayed())
        except Exception, e:
            self._handle_exception(e)

    @unittest.skip('not implemented')
    def test_base_use_case_no_count(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_no_bougth_at(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_no_option_plan(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_same_buyer_seller(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_negative_count(self):
        pass

    @unittest.skip('not implemented')
    def test_base_use_case_negative_Vesting(self):
        pass

    def test_date_save_error_78(self):
        """
        for some date the server stores the day before, for some not
        good: 1.11.2016
        bad: 15.5.2016)
        """

        # initial optionplan and option creation transaction
        self.optionplan = OptionPlanGenerator().generate(
            company=self.operator.company,
            security=self.securities[0]
        )
        PositionGenerator().generate(
            seller=None, buyer=self.operator.company.get_company_shareholder(),
            count=100, security=self.securities[0])
        OptionTransactionGenerator().generate(
            seller=None, buyer=self.operator.company.get_company_shareholder(),
            option_plan=self.optionplan,
            count=self.operator.company.get_company_shareholder().share_count())

        try:

            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_transfer_option()
            app.enter_transfer_option_data(
                buyer=self.buyer,
                title=self.optionplan.title,
                seller=self.operator.company.get_company_shareholder(),
                count=self.operator.company.get_company_shareholder()
                .options_count()
            )
            app.click_save_transfer_option()

            # wait for form to disappear
            app.close_modal('addOptionTransaction')
            app.wait_until_invisible(
                (By.CSS_SELECTOR, '#add_option_transaction'))

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_shown(buyer=self.buyer))
            self.assertTrue(app.is_option_date_equal('13.05.16'))

            app.click_open_transfer_option()
            app.enter_transfer_option_data(
                date=datetime.date(2016, 11, 1), buyer=self.buyer,
                title=self.optionplan.title,
                seller=self.operator.company.get_company_shareholder(),
                count=self.operator.company.get_company_shareholder()
                .options_count()
            )
            app.click_save_transfer_option()

            # wait for form to disappear
            app.close_modal('addOptionTransaction')
            app.wait_until_invisible(
                (By.CSS_SELECTOR, '#add_option_transaction'))

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_shown(buyer=self.buyer))
            self.assertTrue(app.is_option_date_equal('1.11.16'))

        except Exception, e:
            self._handle_exception(e)

    def test_base_options_with_segments(self):
        """
        test with valid data: adding option plan, adding transaction
        assert: initial transaction, all transactions with proper segments
        """
        optiontransactions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        operator = shs[0].company.operator_set.first()
        for sec in operator.company.security_set.all():
            sec.track_numbers = True
            sec.save()

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, operator.user)
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')

            self.assertTrue(app.is_option_plan_form_open())

            app.enter_option_plan_form_data_with_segments()
            app.click_save_option_plan_form()

            # wait for form to disappear
            app.close_modal('addOptionPlan')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_option_plan_displayed(
                OptionPlan.objects.last().security))

            ct = shs[1].option_buyer.count()
            app.click_open_transfer_option()
            app.enter_transfer_option_with_segments_data(
                buyer=shs[1], seller=shs[0], share_count=shs[0].options_count(),
                number_segments="2100,2101,2102-2252")
            app.click_save_transfer_option()

            # wait for form to disappear
            app.close_modal('addOptionTransaction')
            app.wait_until_invisible(
                (By.CSS_SELECTOR, '#add_option_transaction'))

            s = shs[1]
            s.refresh_from_db()
            self.assertEqual(ct + 1, s.option_buyer.count())
            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_with_segments_shown(
                buyer=shs[1], seller=shs[0]
            ))

        except Exception, e:
            self._handle_exception(e)


class OptionsPlanFunctionalTestCase(BaseSeleniumTestCase):

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        self.securities = TwoInitialSecuritiesGenerator().generate(
            company=self.operator.company)
        self.buyer = ShareholderGenerator().generate(
            company=self.operator.company)
        self.seller = ShareholderGenerator().generate(
            company=self.operator.company)

    def test_optionplan_detail_with_segments(self):
        """
        test numbered segments detail on option plan detail page
        """
        optiontransactions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        optionsplan = optiontransactions[0].option_plan
        operator = shs[0].company.operator_set.first()
        for sec in operator.company.security_set.all():
            sec.track_numbers = True
            sec.save()

        try:
            path = reverse('optionplan',
                           kwargs={'optionsplan_id': optionsplan.pk})
            app = page.OptionsPlanDetailPage(
                self.selenium, self.live_server_url, operator.user, path)

            security_text = (
                    u'Vorzugsaktien (100 CHF)\n'
                    u'(Reservierte Aktiennummern 1000-2000)')
            app.wait_until_text_present(
                (By.CSS_SELECTOR, 'div.security div.text'), security_text)

            self.assertEqual(app.get_security_text(), security_text)

        except Exception, e:
            self._handle_exception(e)

    def test_add_optionplan_with_segments_bad_input(self):
        """
        test with invalid data: adding option plan, adding transaction
        assert: initial transaction, all transactions with proper segments
        """
        positions, shs = \
            ComplexPositionsWithSegmentsGenerator().generate()
        operator = shs[0].company.operator_set.first()
        for sec in operator.company.security_set.all():
            sec.track_numbers = True
            sec.save()

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, operator.user)
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')

            self.assertTrue(app.is_option_plan_form_open())

            # empty numbers segments field
            app.enter_option_plan_form_data_with_segments(number_segments='')
            app.click_save_option_plan_form()
            # wait for error
            app.wait_until_visible((
                By.CSS_SELECTOR, '#addOptionPlan .form-error'))
            self.assertEqual(
                app.get_form_errors(),
                [u'Aktiennummern: Ung\xfcltige Aktiennummern. '
                 u'Valide sind: "1,2,3,4-9".']
            )

            # not owned by company shareholder
            app.refresh()
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')
            app.enter_option_plan_form_data_with_segments(
                number_segments='1050', count=1)
            app.click_save_option_plan_form()
            # wait for error
            app.wait_until_visible((
                By.CSS_SELECTOR, '#addOptionPlan .form-error'))

            # attempt to fix unstable @CI
            # FIXME remove once stable
            for s in Shareholder.objects.all():
                print s.current_segments(
                    security=operator.company.security_set.first())
                print s.current_options_segments(
                    security=operator.company.security_set.first())

            self.assertEqual(
                app.get_form_errors(),
                [u'Aktiennummern: Aktiennummer "[1050]" geh\xf6rt nicht zu '
                 u'Verk\xe4ufer "itself". Verf\xfcgbar sind '
                 u'"[u\'1201-1665\', u\'1667-2000\']".'])

            # wrong count vs. segment count
            app.refresh()
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')
            app.enter_option_plan_form_data_with_segments(
                number_segments='1667', count=2)
            app.click_save_option_plan_form()
            # wait for error
            app.wait_until_visible((
                By.CSS_SELECTOR, '#addOptionPlan .form-error'))
            self.assertEqual(
                app.get_form_errors(),
                [u'Anzahl: Anzahl der Aktien in den Aktiennummern ist nicht '
                 u'identisch mit der Anzahl der Aktien im Formular: 1'])

            # successful
            app.refresh()
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')
            app.enter_option_plan_form_data_with_segments(
                number_segments='1667',
                count=1)
            app.click_save_option_plan_form()
            # wait for error to disappear
            app.close_modal('addOptionPlan')
            app.wait_until_invisible((
                By.CSS_SELECTOR, '#addOptionPlan .form-error'))

            # attempt to fix unstable @CI
            # FIXME remove once stable
            for s in Shareholder.objects.all():
                print s.current_segments(
                    security=operator.company.security_set.first())
                print s.current_options_segments(
                    security=operator.company.security_set.first())

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_option_plan_displayed(
                OptionPlan.objects.last().security))

        except Exception, e:
            self._handle_exception(e)

    def test_add_optiontransaction_with_segments_bad_input(self):
        """
        test with invalid data: adding option plan, adding transaction
        assert: initial transaction, all transactions with proper segments
        """
        optionstransactions, shs = \
            ComplexOptionTransactionsWithSegmentsGenerator().generate()
        operator = shs[0].company.operator_set.first()
        for sec in operator.company.security_set.all():
            sec.track_numbers = True
            sec.save()

        try:
            app = page.OptionsPage(
                self.selenium, self.live_server_url, operator.user)
            app.click_open_create_option_plan()
            app.wait_until_modal_opened('addOptionPlan')
            self.assertTrue(app.is_option_plan_form_open())
            app.enter_option_plan_form_data_with_segments()
            app.click_save_option_plan_form()

            # wait for form to disappear
            app.close_modal('addOptionPlan')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))

            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_option_plan_displayed(
                OptionPlan.objects.last().security))

            # not owned by seller
            app.click_open_transfer_option()
            app.enter_transfer_option_with_segments_data(
                buyer=shs[1], seller=shs[0], number_segments='1666',
                share_count=1)
            app.click_save_transfer_option()
            # wait for error
            app.wait_until_visible((By.CSS_SELECTOR, '.form-error'))
            self.assertEqual(
                app.get_form_errors(),
                [u'Aktiennummern: Aktiennummer "[1666]" geh\xf6rt nicht zu '
                 u'Verk\xe4ufer "itself". Verf\xfcgbar sind '
                 u'"[u\'1201-1665\', u\'1667-2000\', u\'2100-2255\']".'])

            # no count match
            app.refresh()
            # wait for angular (tranfer option link)
            app.wait_until_visible(
                (By.CSS_SELECTOR,
                 '[ng_controller="OptionsController"] .panel .btn'))
            app.click_open_transfer_option()
            app.enter_transfer_option_with_segments_data(
                buyer=shs[1], seller=shs[0], number_segments='1667',
                share_count=12)
            app.click_save_transfer_option()
            # wait for error
            app.wait_until_visible((By.CSS_SELECTOR, '.form-error'))
            self.assertEqual(
                app.get_form_errors(),
                [u'Anzahl: Anzahl der Aktien in den Aktiennummern ist nicht '
                 u'identisch mit der Anzahl der Aktien im Formular: 1'])

            # not with option plan segments
            """ NOT VALID
            app.refresh()
            app.click_open_transfer_option()
            app.enter_transfer_option_with_segments_data(
                buyer=shs[1], seller=shs[0], number_segments='3001',
                share_count=1)
            app.click_save_transfer_option()
            self.assertEqual(
                app.get_form_errors(),
                [u'Anzahl: Anzahl der Aktien in den Aktiennummern ist nicht '
                 u'identisch mit der Anzahl der Aktien im Formular: 1'])
            """

            # success
            app.refresh()
            # wait for angular (tranfer option link)
            app.wait_until_visible(
                (By.CSS_SELECTOR,
                 '[ng_controller="OptionsController"] .panel .btn'))
            app.click_open_transfer_option()
            app.enter_transfer_option_with_segments_data(
                buyer=shs[1], seller=shs[0], share_count=shs[0].options_count(),
                number_segments="2100,2101,2102-2252")
            app.click_save_transfer_option()
            # wait for form to disappear
            app.close_modal('addOptionTransaction')
            app.wait_until_invisible(
                (By.CSS_SELECTOR, '#add_option_transaction'))
            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue(app.is_transfer_option_with_segments_shown(
                buyer=shs[1], seller=shs[0]
            ))
        except Exception, e:
            self._handle_exception(e)

    def test_click_detail(self):

        # initial pos
        OptionTransactionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0], registration_type='2')

        try:

            app = page.OptionsPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_optiontransaction()

            app.wait_until_visible((By.ID, "optiontransaction-detail"))
            self.assertEqual(
                app.wait_until_visible((By.CLASS_NAME, 'registration-type'))
                .find_elements_by_class_name('td')[1].text,
                _('Personal representation'))

        except Exception, e:
            self._handle_exception(e)


class PositionFunctionalTestCase(BaseSeleniumTestCase):
    """
    test all core position funcs
    logic is tested in api, this here covers mainly FE logic
    """

    def setUp(self):
        self.operator = OperatorGenerator().generate()
        company = self.operator.company
        self.securities = TwoInitialSecuritiesGenerator().generate(
            company=company)
        self.buyer = ShareholderGenerator().generate(company=company)
        self.seller = ShareholderGenerator().generate(company=company)
        self.seller2 = ShareholderGenerator().generate(company=company)
        # initial position for each sec
        PositionGenerator().generate(
            buyer=self.seller,
            security=self.securities[1], number_segments=[u'0-9999'],
            count=10000, seller=None)
        PositionGenerator().generate(
            buyer=self.seller,
            security=self.securities[0], number_segments=[u'0-9999'],
            count=10000, seller=None)

    def test_add(self):
        """
        add position
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            app.enter_new_position_data(position)
            app.click_save_position()

            # wait for form to disappear
            app.close_modal('addPosition')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_position'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())
            # ('%-d.%-m.%y') in case leading zero is not needed
            self.assertIn(datetime.datetime.today().strftime('%-d.%m.%y'),
                          app.get_position_row_data()[0].split('\n')[0])

            app.refresh()
            # wait for table
            app.wait_until_visible(
                (By.CSS_SELECTOR, '#positions .table .position'))
            self.assertEqual(app.get_position_row_data()[0].split('\n')[0],
                             datetime.datetime.today().strftime('%-d.%m.%y'))

        except Exception, e:
            self._handle_exception(e)

    def test_add_optional_fields(self):
        """
        add position
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1], stock_book_id='444', depot_type='1',
            certificate_id='88888')

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            app.show_optional_fields()
            app.enter_new_position_data(position)
            app.click_save_position()

            # wait for form to disappear
            app.close_modal('addPosition')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_position'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())
            # ('%-d.%-m.%y') in case leading zero is not needed
            self.assertIn(datetime.datetime.today().strftime('%-d.%m.%y'),
                          app.get_position_row_data()[0].split('\n')[0])
            position = Position.objects.last()
            self.assertEqual(position.stock_book_id, '444')
            self.assertEqual(position.depot_type, '0')
            self.assertEqual(position.certificate_id, '88888')

        except Exception, e:
            self._handle_exception(e)

    def test_add_96(self):
        """
        add position with floating point value and large count
        """
        # seed sufficient amout of shares
        PositionGenerator().generate(
            buyer=self.seller, seller=None, security=self.securities[1],
            count=15000000)

        # template object
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])
        position.value = 4.55
        position.count = 15000000
        count = Position.objects.count()
        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            app.enter_new_position_data(position)
            app.click_save_position()

            # wait for form to disappear
            app.close_modal('addPosition')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_position'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

            position = Position.objects.latest('pk')
            self.assertEqual(count + 1, Position.objects.count())
            self.assertEqual(position.value, Decimal('4.55'))
            self.assertEqual(position.count, 15000000)

        except Exception, e:
            self._handle_exception(e)

    def test_add_numbered_segments(self):
        """
        add position with numbered shares
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1], count=6)

        for s in self.securities:
            s.track_numbers = True
            s.save()

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            app.enter_new_position_data(position)
            app.click_save_position()

            # wait for form to disappear
            app.close_modal('addPosition')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_position'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())
            self.assertTrue('0, 1-2, 999-1001' in self.selenium.page_source)

        except Exception, e:
            self._handle_exception(e)

    def test_add_numbered_segments_with_segment_lookup(self):
        """
        add position with numbered shares and lookup for a shareholder
        what numbers are available
        test  trigger:
        * on change for seller, security, date
        test result
        * number segments, none
        """
        # position unsaved for data seeding
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1], count=6)

        # make one of two secs with number tracking
        s = self.operator.company.security_set.get(title='C')
        s.track_numbers = True
        s.save()

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            # wait for table
            app.wait_until_visible((By.CSS_SELECTOR, '#positions .table .tr'))
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')

            # test cycle: w/ date, seller, sec
            app.enter_bought_at(position.bought_at)
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_typeahead('add_position', position.seller, 'seller')
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_security(position.security, 'add-position-form')
            self.assertTrue(app.has_available_segments_tooltip())
            self.assertEqual(app.get_segment_from_tooltip(), u'0,1-9999')

            app.refresh()
            # wait for table
            app.wait_until_visible((By.CSS_SELECTOR, '#positions .table .tr'))
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            # test w/ sec + seller
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_typeahead('add_position', position.seller, 'seller')
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_security(position.security, 'add-position-form')
            self.assertTrue(app.has_available_segments_tooltip())

            app.refresh()
            # wait for table
            app.wait_until_visible((By.CSS_SELECTOR, '#positions .table .tr'))
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            # test no segs avail
            position.seller = self.seller2
            app.enter_bought_at(position.bought_at)
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_typeahead('add_position', position.seller, 'seller')
            self.assertFalse(app.has_available_segments_tooltip())
            app.enter_security(position.security, 'add-position-form')
            self.assertTrue(app.has_available_segments_tooltip())
            self.assertTrue(app.has_available_segments_tooltip_nothing_found())

        except Exception, e:
            self._handle_exception(e)

    def test_add_numbered_segments_invalid(self):
        """
        add position with numbered shares
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])

        for s in self.securities:
            s.track_numbers = True
            s.save()

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            # wait for table
            app.wait_until_visible((By.CSS_SELECTOR, '#positions .table .tr'))
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            app.enter_new_position_data(position)

            # clear numbers segment field
            el = self.selenium.find_element_by_id('add_position')
            form = el.find_element_by_tag_name('form')
            input = form.find_elements_by_tag_name('input')[5]
            input.clear()

            app.click_save_position()

            # wait for error
            app.wait_until_visible((By.CSS_SELECTOR, '.form-error'))

            self.assertFalse(app.is_no_errors_displayed())

            # add [A-Z] number segments
            el = self.selenium.find_element_by_id('add_position')
            form = el.find_element_by_tag_name('form')
            input = form.find_elements_by_tag_name('input')[5]
            input.send_keys('AA')

            app.click_save_position()

            self.assertFalse(app.is_no_errors_displayed())

            # add valid number segments
            el = self.selenium.find_element_by_id('add_position')
            form = el.find_element_by_tag_name('form')
            input.clear()
            input = form.find_elements_by_tag_name('input')[5]
            input.send_keys('1,2,3')

            app.click_save_position()

            # wait for form to disappear
            app.close_modal('addPosition')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_position'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_add_error_no_value(self):
        """
        confirm form error handling
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')

            # enter empty data
            position.count = None
            position.value = None
            app.enter_new_position_data(position)
            app.click_save_position()

            # wait for error
            app.wait_until_visible((By.CSS_SELECTOR, '.form-error'))

            self.assertFalse(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_add_error_large_numbers(self):
        """
        confirm form error handling
        """
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            # enter data too large
            position.count = 99999999991
            position.value = 99999599999
            app.enter_new_position_data(position)
            app.click_save_position()
            time.sleep(3)
            self.assertTrue(
                self.selenium.find_element_by_xpath(
                    '//p[contains(@class, "form-error")]').is_displayed()
                )
            # self.assertFalse(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_add_error_matching_numbers(self):
        """
        confirm form error handling
        """
        # seed more positions
        PositionGenerator().generate(
            buyer=self.seller, seller=None, count=88888888,
            security=self.securities[1])
        # position template
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[1])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_add_position_form()
            app.wait_until_modal_opened('addPosition')
            # working data
            position.count = 88888888
            position.value = 22222222
            app.enter_new_position_data(position)
            app.click_save_position()

            # wait for form to disappear
            app.close_modal('addPosition')
            app.wait_until_invisible((By.CLASS_NAME, 'add_position'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_cap_increase(self):
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_cap_increase_form()
            app.wait_until_modal_opened('capitalForm')
            app.enter_new_cap_data(position)
            app.click_save_cap_increase()

            # wait for form to disappear
            app.close_modal('capitalForm')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_capital'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_cap_increase_96(self):
        position = PositionGenerator().generate(
            save=False, seller=self.seller, buyer=self.buyer,
            security=self.securities[0])
        position.value = 4.55
        position.count = 15000000

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_cap_increase_form()
            app.wait_until_modal_opened('capitalForm')
            app.enter_new_cap_data(position)
            app.click_save_cap_increase()

            # wait for form to disappear
            app.close_modal('capitalForm')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_capital'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

            position = Position.objects.latest('pk')
            self.assertEqual(position.value, Decimal('4.55'))
            self.assertEqual(position.count, 15000000)
        except Exception, e:
            self._handle_exception(e)

    def test_cap_increase_numbered_segments(self):
        """
        capital increase with numbered segments
        """
        position = PositionGenerator().generate(
            save=False, security=self.securities[1], count=6,
            number_segments='1, 2, 3, 5-7')

        for s in self.securities:
            s.track_numbers = True
            s.save()

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_cap_increase_form()
            app.wait_until_modal_opened('capitalForm')
            app.enter_new_cap_data(position)
            app.click_save_cap_increase()

            # wait for form to disappear
            app.close_modal('capitalForm')
            app.wait_until_invisible((By.CSS_SELECTOR, '#add_capital'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())
            position2 = Position.objects.latest('id')
            self.assertEqual([u'1-3', u'5-7'], position2.number_segments)
            self.assertEqual([u'1-3', u'5-7'],
                             position2.security.number_segments)

        except Exception, e:
            self._handle_exception(e)

    def test_split(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])
        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_split_form()
            app.enter_new_split_data(2, 3, 'test comment')
            app.click_save_split()

            # wait for form to disappear
            app.close_modal(id='splitShares')
            app.wait_until_invisible((By.CSS_SELECTOR, '#split-shares'))

            self.assertEqual(len(app.get_position_row_data()), 8)
            self.assertTrue(app.is_no_errors_displayed())

        except Exception, e:
            self._handle_exception(e)

    def test_split_warning_for_numbered_shares(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_open_split_form()
            self.assertFalse(app.has_split_warning_for_numbered_shares())

            s = self.operator.company.security_set.get(title='C')
            s.track_numbers = True
            s.save()

            app.refresh()
            # wait for table
            app.wait_until_visible(
                (By.CSS_SELECTOR, '#positions .table .position'))
            app.click_open_split_form()
            app.wait_until_visible((By.CLASS_NAME, 'alert-warning'))
            self.assertTrue(app.has_split_warning_for_numbered_shares())

        except Exception, e:
            self._handle_exception(e)

    def test_delete(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            time.sleep(1)
            app.click_delete_position()

            # header, row, 2x split
            self.assertEqual(app.get_position_row_count(), 3)

        except Exception, e:
            self._handle_exception(e)

    def test_confirm(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0])

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_confirm_position()

            self.assertEqual(app.count_draft_mode_items(), 0)

        except Exception, e:
            self._handle_exception(e)

    def test_click_detail(self):

        # initial pos
        PositionGenerator().generate(
            seller=self.seller, buyer=self.buyer,
            security=self.securities[0], registration_type='2')

        try:

            app = page.PositionPage(
                self.selenium, self.live_server_url, self.operator.user)
            app.click_position()

            app.wait_until_visible((By.ID, "position-detail"))
            self.assertEqual(
                app.wait_until_visible((By.CLASS_NAME, 'registration-type'))
                .find_elements_by_class_name('td')[1].text,
                _('Personal representation'))

        except Exception, e:
            self._handle_exception(e)
