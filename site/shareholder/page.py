"""
learned from here
http://selenium-python.readthedocs.org/en/latest/page-objects.html
"""

# from element import BasePageElement (save all locators here)
# from locators import MainPageLocators (save all setter/getter here)

import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from project.generators import DEFAULT_TEST_DATA
from project.page import BasePage

from utils.formatters import human_readable_segments

logger = logging.getLogger(__name__)


class BaseDetailPage(BasePage):

    def __init__(self, driver, live_server_url, user, path=None):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(BaseDetailPage, self).__init__(driver)

        # login and load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username,
                   password=DEFAULT_TEST_DATA['password'])

        assert 'start' in self.driver.current_url, 'login not successful'

        if path:
            self.get('%s%s' % (live_server_url, path))
        else:
            self.get('%s%s' % (live_server_url))

    def get_field(self, cls):
        """
        returns string for class
        """
        return self.driver.find_element_by_class_name(cls).text


class ShareholderDetailPage(BaseDetailPage):

    def click_to_edit(self, class_name):
        el = self.wait_until_visible((
            By.XPATH,
            u'//div[contains(@class, "{}")]//'
            u'span[contains(@class, "editable-click")]'.format(class_name)
        ))
        el.click()

    def edit_field(self, value, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-input')
        el.clear()
        el.send_keys(str(value))

    def select_type(self, class_name, legal_type):
        row = self.driver.find_element_by_class_name(class_name)
        select = row.find_element_by_tag_name('select')
        select = Select(select)
        select.select_by_visible_text(legal_type)

    # --- GET DATA
    def get_birthday(self, class_name="birthday"):
        """
        return date from inside this element
        """
        bday = self.driver.find_element_by_xpath(
            '//div[contains(@class, "birthday")]//div//span')
        return bday.text

    def get_securities(self):
        """
        returns list of securities from page
        """
        secs = []
        t = self.driver.find_element_by_xpath(
            '//div[contains(@class, "stock") and contains(@class, "table")]')
        for tr in t.find_elements_by_class_name('security'):
            if tr.find_elements_by_class_name('number-segments'):
                segments = tr.find_element_by_class_name(
                               'number-segments').text
            else:
                segments = u''
            secs.extend([
                tr.find_element_by_class_name('count').text,
                segments
                ])

        return secs

    # --- trigger buttons
    def save_edit(self, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-buttons')
        el = el.find_element_by_tag_name('button')
        el.click()


class PositionDetailPage(BaseDetailPage):
    pass


class OptionTransactionDetailPage(BaseDetailPage):
    pass


class OptionsPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(OptionsPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username,
                   password=DEFAULT_TEST_DATA['password'])
        self.get('%s%s' % (live_server_url, '/options/'))

    # -- INPUT COMMANDs
    def enter_option_plan_form_data(self, *args, **kwargs):
        el = self.driver.find_element_by_id('add_option_plan')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        select = Select(selects[0])
        select.select_by_index(2)

        self.use_datepicker(class_name='add-optionplan',
                            date=DEFAULT_TEST_DATA.get('date_obj'))
        # inputs[0].send_keys(DEFAULT_TEST_DATA.get('date'))
        inputs[1].send_keys(DEFAULT_TEST_DATA.get('title'))
        inputs[2].send_keys(
            str(kwargs.get('exercise_price',
                           DEFAULT_TEST_DATA.get('exercise_price'))))
        inputs[3].send_keys(str(
            kwargs.get('count', DEFAULT_TEST_DATA.get('share_count'))))
        inputs[5].send_keys(DEFAULT_TEST_DATA.get('comment'))

    def enter_option_plan_form_data_with_segments(self, **kwargs):
        el = self.driver.find_element_by_id('add_option_plan')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        select = Select(selects[0])
        select.select_by_index(2)

        self.use_datepicker(class_name='add-optionplan',
                            date=DEFAULT_TEST_DATA.get('date_obj'))
        # inputs[0].send_keys(DEFAULT_TEST_DATA.get('date'))
        inputs[1].send_keys(DEFAULT_TEST_DATA.get('title'))
        inputs[2].send_keys(DEFAULT_TEST_DATA.get('exercise_price'))
        inputs[3].send_keys(kwargs.get('count',
                                       DEFAULT_TEST_DATA.get('share_count')))
        inputs[4].send_keys(kwargs.get('number_segments',
                                       DEFAULT_TEST_DATA.get('number_segments'))
                            )
        inputs[5].send_keys(DEFAULT_TEST_DATA.get('comment'))

    def enter_transfer_option_data(self, **kwargs):
        el = self.driver.find_element_by_id('add_option_transaction')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        buyer = kwargs.get('buyer')
        seller = kwargs.get('seller')

        if buyer:
            self.enter_typeahead('add_option_transaction', buyer, 'buyer')
        if seller:
            self.enter_typeahead('add_option_transaction', seller, 'seller')

        time.sleep(1)
        select = Select(selects[0])
        select.select_by_visible_text(
            kwargs.get('title') or DEFAULT_TEST_DATA.get('title'))

        self.use_datepicker(
            class_name='add-option',
            date=kwargs.get('date') or DEFAULT_TEST_DATA.get('date_obj'))
        #inputs[0].send_keys(
        #    kwargs.get('date') or DEFAULT_TEST_DATA.get('date'))
        inputs[3].send_keys(str(
            kwargs.get('count', DEFAULT_TEST_DATA.get('count'))))
        inputs[5].send_keys(DEFAULT_TEST_DATA.get('vesting_period'))

        if kwargs.get('depot_type'):
            select = Select(selects[1])
            select.select_by_visible_text('Gesellschaftsdepot')

        if kwargs.get('stock_book_id'):
            inputs[6].clear()
            inputs[6].send_keys(kwargs.get('stock_book_id'))

        if kwargs.get('certificate_id'):
            inputs[7].clear()
            inputs[7].send_keys(kwargs.get('certificate_id'))

    def enter_transfer_option_with_segments_data(self, **kwargs):
        el = self.driver.find_element_by_id('add_option_transaction')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        buyer = kwargs.get('buyer')
        seller = kwargs.get('seller')

        if buyer:
            self.enter_typeahead('add_option_transaction', buyer, 'buyer')
        if seller:
            self.enter_typeahead('add_option_transaction', seller, 'seller')

        time.sleep(1)
        select = Select(selects[0])
        select.select_by_visible_text(
            kwargs.get('title') or DEFAULT_TEST_DATA.get('title'))

        self.use_datepicker(
            class_name='add-option',
            date=kwargs.get('date') or DEFAULT_TEST_DATA.get('date_obj'))
        # inputs[0].send_keys(
        #    kwargs.get('date') or DEFAULT_TEST_DATA.get('date'))
        inputs[3].send_keys(kwargs.get('share_count',
                            DEFAULT_TEST_DATA.get('share_count')))
        inputs[4].send_keys(kwargs.get('number_segments',
                            DEFAULT_TEST_DATA.get('number_segments')))
        inputs[5].send_keys(DEFAULT_TEST_DATA.get('vesting_period'))

    # -- CLICKs
    def click_optiontransaction(self):
        row = self.wait_until_visible((By.CLASS_NAME, 'optiontransaction'))
        row.click()

    def click_open_create_option_plan(self):
        time.sleep(2)
        el = self.driver.find_element_by_link_text(
            "Neuen Optionsplan erstellen")
        el.click()

    def click_save_option_plan_form(self):
        el = self.driver.find_element_by_id('add_option_plan')
        div = el.find_elements_by_class_name('form-group')[1]
        button = div.find_elements_by_tag_name('button')[1]
        button.click()

    def click_open_transfer_option(self):
        el = self.driver.find_element_by_link_text(u"Optionen \xfcbertragen")
        el.click()

    def click_save_transfer_option(self):
        el = self.driver.find_element_by_xpath(
            '//button[contains(@class, "btn-focus")]')
        el.click()

    def show_optional_fields(self):
        self.driver.find_element_by_class_name('el-icon-plus-sign').click()

    # -- VALIDATIONs
    def is_option_plan_form_open(self):
        return self._is_element_displayed(id='add_option_plan')

    def is_option_plan_displayed(self, security):
        self.wait_until_visible((By.TAG_NAME, "h2"))
        h2s = self.driver.find_elements_by_tag_name('h2')
        string = u"Optionsplan: {} f\xfcr {}".format(
            DEFAULT_TEST_DATA.get('title'),
            security)
        for h2 in h2s:
            if string in h2.text:
                return True
        # for debugging
        extra = {
            'heading_strings': [h2.text for h2 in h2s],
            'needle': string}
        logger.warning('option plan heading not found', extra=extra)
        print extra

        return False

    def is_transfer_option_shown(self, **kwargs):
        for table in self.driver.find_elements_by_class_name('table'):
            for tr in table.find_elements_by_class_name('optiontransaction'):
                s = kwargs.get('buyer').get_full_name()
                if s == tr.find_element_by_class_name('buyer-name').text:
                    return True
                print s, '>', tr.find_element_by_class_name('buyer-name').text

        return False

    def is_transfer_option_with_segments_shown(self, **kwargs):
        buyer = kwargs.get('buyer')
        ot = buyer.option_buyer.latest('id')
        s1 = buyer.get_full_name()
        for table in self.driver.find_elements_by_class_name('table'):
            trs = table.find_elements_by_class_name("optiontransaction")
            for tr in trs:
                buyer_td = tr.find_element_by_class_name('buyer-name')
                count_td = tr.find_element_by_class_name('count')
                if (
                    s1 == buyer_td.text and str(ot.count) in count_td.text and
                    human_readable_segments(ot.number_segments)
                    in count_td.text
                ):
                    return True
                print s1, buyer_td.text, count_td.text

        return False

    def is_option_date_equal(self, date):
        """
        return the date from the markup to the test for verification

        date must be string
        """
        for table in self.driver.find_elements_by_class_name('table'):
            for td in table.find_elements_by_class_name('td'):
                div = td.find_elements_by_class_name('bought-at')
                if len(div) > 0 and div[0].text == date:
                    return True
        return False

    def is_shareholder_name_displayed(self, shareholder):
        """
        does the shareholders full name exist inside the markup
        """
        return shareholder.get_full_name() in self.driver.page_source

    # --  aggregations of logic
    def prepare_optionplan_fixtures(self):
        """ setup options plan """
        self.click_open_create_option_plan()

        self.enter_option_plan_form_data()
        self.click_save_option_plan_form()

        # wait for form to disappear
        self.wait_until_invisible((By.CSS_SELECTOR, '#add_option_plan'))


class OptionsPlanDetailPage(BasePage):
    """Options Detail View"""

    def __init__(self, driver, live_server_url, user, path):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(OptionsPlanDetailPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username,
                   password=DEFAULT_TEST_DATA['password'])
        self.get('%s%s' % (live_server_url, path))

    def get_security_text(self):
        """
        return text of security table element
        """
        el = self.driver.find_element_by_xpath(
            '//div[contains(@class, "security")]'
            '//div[contains(@class, "text")]')
        return el.text


class PositionPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(PositionPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username,
                   password=DEFAULT_TEST_DATA['password'])
        self.get('%s%s' % (live_server_url, '/positions/'))

    def click_confirm_position(self):
        table = self.driver.find_element_by_class_name('table')
        time.sleep(2)  # FIXME
        trs = table.find_elements_by_class_name('tr')
        row = trs[2]
        td = row.find_elements_by_class_name('td')[-1]
        td.find_elements_by_tag_name('a')[1].click()

    def click_delete_position(self):
        table = self.driver.find_element_by_class_name('table')
        time.sleep(1)  # FIXME
        trs = table.find_elements_by_class_name('tr')
        row = trs[2]
        td = row.find_elements_by_class_name('td')[-1]
        td.find_element_by_tag_name('a').click()

    def click_position(self):
        row = self.wait_until_visible((By.CLASS_NAME, 'position'))
        row.click()

    def click_open_add_position_form(self):
        btn = self.driver.find_element_by_class_name('add-position')
        btn.click()

    def click_open_split_form(self):
        btn = self.driver.find_element_by_class_name('split-shares')
        btn.click()

    def click_open_cap_increase_form(self):
        btn = self.driver.find_element_by_class_name('add-capital')
        btn.click()

    def click_save_cap_increase(self):
        btn = self.driver.find_element_by_class_name('save-capital')
        btn.click()

    def click_save_position(self):
        btn = self.driver.find_element_by_class_name('save-position')
        btn.click()

    def click_save_split(self):
        btn = self.driver.find_element_by_class_name('save-split')
        btn.click()

    def enter_new_position_data(self, position):
        el = self.driver.find_element_by_id('add_position')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        # select elements: seller, buyer, security - before inputs to have magic
        # working
        time.sleep(2)  # FIXME

        self.enter_typeahead('add_position', position.seller, 'seller')
        self.enter_typeahead('add_position', position.buyer, 'buyer')

        self.enter_security(position.security, 'add-position-form')
        self.enter_bought_at(position.bought_at)

        # count
        if position.count:
            inputs[3].clear()  # clear existing values
            # enter in two chunks. attempt to avoid browser moving to next
            # input on CI
            inputs[3].send_keys(str(position.count)[:5])  # count
            inputs[3].send_keys(str(position.count)[5:])

        # value
        if position.value:
            inputs[4].clear()  # clear existing values
            inputs[4].send_keys(str(position.value))  # price

        # if numbered shares enter segment
        if position.security.track_numbers:
            inputs[5].clear()
            inputs[5].send_keys('0,1,2,999-1001')

        inputs[6].clear()  # clear existing values
        inputs[6].send_keys(position.comment)  # comment

        if position.depot_type:
            select = Select(selects[1])
            select.select_by_visible_text('Gesellschaftsdepot')

        if position.stock_book_id:
            inputs[7].clear()
            inputs[7].send_keys(position.stock_book_id)

        if position.certificate_id:
            inputs[9].clear()
            inputs[9].send_keys(position.certificate_id)

    def show_optional_fields(self):
        self.driver.find_element_by_class_name('el-icon-plus-sign').click()

    def enter_bought_at(self, date):
        """
        enter position.bought_at in form
        """
        time.sleep(1)  # FIXME

        # input #0 use datepicker
        self.use_datepicker('add-position-form', None)

    def enter_security(self, security, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        form = el.find_element_by_tag_name('form')
        select = form.find_element_by_class_name('security')

        select = Select(select)
        select.select_by_visible_text(unicode(security))

    def enter_new_cap_data(self, position):

        el = self.driver.find_element_by_id('add_capital')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')

        # input #0 use datepicker
        self.use_datepicker('add-capital-form', None)
        self.enter_security(position.security, 'add-capital-form')

        if position.count:
            inputs[1].clear()
            inputs[1].send_keys(str(position.count))  # count
        if position.value:
            inputs[2].clear()
            inputs[2].send_keys(str(position.value))  # price
        if inputs[3].is_displayed():
            inputs[3].clear()
            inputs[3].send_keys(position.number_segments)  # comment
        inputs[4].clear()
        inputs[4].send_keys(position.comment)  # comment

    def enter_new_split_data(self, *args):
        el = self.driver.find_element_by_id('split-shares')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        selects = form.find_elements_by_tag_name('select')

        # input #0 use datepicker
        self.use_datepicker('split-shares-form', None)
        inputs[1].send_keys(args[0])  # dividend
        inputs[2].send_keys(args[1])  # divisor
        inputs[3].send_keys(args[2])  # comment

        # select elements: seller, buyer, security
        for select in selects:
            select = Select(select)
            select.select_by_index(1)

    def get_position_row_data(self):
        """
        return list of data from position in single row of table
        """
        table = self.driver.find_element_by_class_name('table')
        time.sleep(1)  # FIXME
        trs = table.find_elements_by_class_name('tr')
        row = trs[2]
        return [td.text for td in row.find_elements_by_class_name('td')]

    def get_position_row_count(self):
        table = self.driver.find_element_by_class_name('table')
        time.sleep(1)  # FIXME
        trs = table.find_elements_by_class_name('tr')
        return [tr.is_displayed() for tr in trs].count(True)

    def get_segment_from_tooltip(self):
        """
        extract segment string from tooltip
        """
        el = self.driver.find_element_by_id('add_position')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')

        els = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "popover-content")]')

        if inputs[3].is_displayed() and not els:
            inputs[3].click()
            els = self.driver.find_elements_by_xpath(
                '//div[contains(@class, "popover-content")]')

        return els[0].text.split(':')[1].strip()

    def count_draft_mode_items(self):
        table = self.driver.find_element_by_class_name('table')
        time.sleep(1)
        trs = table.find_elements_by_class_name('tr')
        row = trs[2]
        return row.find_element_by_class_name('td').text.count('Entwurf')

    def has_available_segments_tooltip(self):
        """
        check of tooltip bubble on segment field is shown
        shown only when number_segment fild is selected
        """
        el = self.driver.find_element_by_id('add_position')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')
        popover_xpath = ('//div[@class="add-position-form"]'
                         '//div[contains(@class,"popover")]')

        els = self.driver.find_elements_by_xpath(popover_xpath)
        time.sleep(1)

        # tooltip is active on click and stays like that. detect if opened or
        # attempt to set element active
        if inputs[5].is_displayed() and not els:
            inputs[5].click()
            time.sleep(2)
            els = self.driver.find_elements_by_xpath(popover_xpath)

        return bool(els and els[0].is_displayed())

    def has_available_segments_tooltip_nothing_found(self):
        """
        check if we show that no available segment was found
        """
        el = self.driver.find_element_by_id('add_position')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')

        els = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "popover-content")]')

        if inputs[3].is_displayed() and not els:
            inputs[3].click()
            els = self.driver.find_elements_by_xpath(
                '//div[contains(@class, "popover-content")]')

        return bool(els and 'keine Aktien' in els[0].text)

    def has_split_warning_for_numbered_shares(self):
        """
        number tracking is not built for split shares
        """
        el = self.driver.find_element_by_id('split-shares')
        return el.find_element_by_class_name('alert-warning').is_displayed()
