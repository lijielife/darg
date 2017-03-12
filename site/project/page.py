#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
learned from here
http://selenium-python.readthedocs.org/en/latest/page-objects.html
"""
import random
import time
from datetime import datetime

from django.conf import settings

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


# from element import BasePageElement (save all locators here)
# from locators import MainPageLocators (save all setter/getter here)

# from selenium.webdriver.support.ui import Select
from project.generators import DEFAULT_TEST_DATA


class BasePage(object):
    """Base class to initialize the base page that will be called
    from all pages"""

    def __init__(self, driver):
        self.driver = driver
        # self.driver.implicitly_wait(settings.TEST_WEBDRIVER_IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(
            settings.TEST_WEBDRIVER_PAGE_LOAD_TIMEOUT)

    def _is_element_displayed(self, **kwargs):

        time.sleep(3)  # FIXME

        if kwargs.get('cls'):
            els = self.driver.find_elements_by_class_name(
                kwargs.get('cls')
            )
        if kwargs.get('id'):
            els = self.driver.find_elements_by_id(
                kwargs.get('id')
            )
        if not len(els):
            return False

        for el in els:
            if el.is_displayed():
                return True

        return False

    def get(self, url):
        """
        run x attempts to fetch url. url must be absolute
        """
        # if TimeoutException happens keep trying
        attempts = 0
        while attempts < 10:
            try:
                self.get(url)
                break
            except TimeoutException:
                attempts += 1

    def login(self, username, password):
        """ log the user in """
        self.get('%s%s' % (self.live_server_url, '/account/login/'))
        self.wait_until_visible((
            By.XPATH,
            '//*[@id="id_auth-username"]'
        )).send_keys(username)
        self.wait_until_visible((
            By.XPATH,
            '//*[@id="id_auth-password"]'
        )).send_keys(password)
        self.wait_until_visible((
            By.XPATH,
            '//button[contains(@class, "btn-primary")]'
        )).click()
        time.sleep(1)  # wait for page reload  # FIXME
        page_heading = self.driver.find_element_by_tag_name('h1').get_attribute(
            'innerHTML')
        assert page_heading == 'Willkommen {}!'.format(
            username), 'failed to login. got {} page instead'.format(
            page_heading)

    def refresh(self):
        """ reload page """
        self.driver.refresh()

    def use_datepicker(self, class_name, date=None):
        """
        use default datepicker to select a date
        """
        self.click_open_datepicker(class_name)
        self.click_date_in_datepicker(class_name, date)

    def click_open_datepicker(self, class_name):
        """
        click to open the datepicker for element X
        """
        el = self.driver.find_element_by_class_name(class_name)
        btns = el.find_elements_by_xpath(
            '//*[contains(@class, "date-field")]//'
            'span[@class="input-group-btn"]//button'
        )
        for btn in btns:
            if btn.is_displayed():
                btn.click()
                # wait until rendered
                self.wait_until_present((By.CLASS_NAME, 'uib-datepicker-popup'))
                return

        raise Exception('Clickable button not found')

    def click_datepicker_next_month(self):
        # handle multiple datepickers
        next_btns = self.driver.find_selement_by_xpath(
            '//div[contains(@class, "uib-datepicker")]//thead//th[3]//button')
        for next_btn in next_btns:
            if next_btn.is_displayed():
                next_btn.click()
                return

    def click_datepicker_previous_month(self):
        # handle multiple datepickers
        next_btns = self.driver.find_selement_by_xpath(
            '//div[contains(@class, "uib-datepicker")]//thead//th[1]//button')
        for next_btn in next_btns:
            if next_btn.is_displayed():
                next_btn.click()
                return

    def click_date_in_datepicker(self, class_name, date=None):
        """
        select some date in datepicker

        click first day of current month
        """
        today = datetime.now().date()
        if not date:
            date = today

        # future month
        if date.month != today.month or date.year != today.year:
            delta = date.month - today.month + 12 * (date.year - today.year)
            for x in range(0, abs(delta)):
                if delta > 0:
                    self.click_datepicker_next_month()
                    time.sleep(0.5)  # FIXME
                else:
                    self.click_datepicker_previous_month()
                    time.sleep(0.5)  # FIXME

        # get day rows
        el = self.driver.find_element_by_class_name(class_name)
        dp_rows = el.find_elements_by_xpath(
            '//table[@class="uib-daypicker"]//tr[@class="uib-weeks ng-scope"]')

        # in case we have multiple dps
        time.sleep(1)  # FIXME
        for dp_row in dp_rows:
            if not dp_row.is_displayed():
                continue
            # go through day tds and find the day to click
            for td in dp_row.find_elements_by_tag_name('td'):
                el2 = td.find_elements_by_tag_name('span')
                if (
                    el2 and el2[0].get_attribute('innerHTML') ==
                    datetime.strftime(date, '%d') and
                    'text-muted' not in el2[0].get_attribute('class')
                ):
                    el2[0].click()
                    return

        raise Exception('Clickable button not found')

    def enter_typeahead(self, id, shareholder, cls):
        """
        enter selling shareholder
        """
        # trigger typeahead search
        el = self.driver.find_element_by_id(id)
        form = el.find_element_by_tag_name('form')
        field = form.find_element_by_class_name(cls)
        field.send_keys(shareholder.get_full_name()[:10])

        # select typeahead result
        self.wait_until_present(
            (By.CSS_SELECTOR, "#{} form .dropdown-menu".format(id)))
        self.wait_until_text_present(
            (By.CSS_SELECTOR, '#{} form .dropdown-menu li a'.format(id)),
            shareholder.get_full_name())
        self.wait_until_clickable(
            (By.CSS_SELECTOR, '#{} form .dropdown-menu li a'.format(id))
        ).click()

    def get_form_errors(self):
        """
        finds elements with .form-error and returns contained string
        """
        els = self.driver.find_elements_by_class_name('form-error')
        return [el.text for el in els if el.is_displayed()]

    def is_no_errors_displayed(self):
        """ MUST not find it, hence exception is True :) """
        return not self._is_element_displayed(cls='alert-danger')

    def scroll_to(self, Y=None, element=None):
        """
        scroll to element or coordinate
        """
        if element:

            y = element.location['y']
            self.driver.execute_script(
                'window.scrollTo(0, {0} - 320)'.format(y))
            ActionChains(self.driver).move_to_element(element).perform()

        else:
            self.driver.execute_script("window.scrollTo(0, {})".format(Y))

    def wait_until_clickable(self, element):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, settings.TEST_WEBDRIVER_WAIT_TIMEOUT)
        element = wait.until(EC.element_to_be_clickable(element))
        return element

    def wait_until_visible(self, element):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, settings.TEST_WEBDRIVER_WAIT_TIMEOUT)
        if isinstance(element, WebElement):
            element = wait.until(EC.visibility_of(element))
        else:
            element = wait.until(EC.visibility_of_element_located(element))
        return element

    def wait_until_invisible(self, element):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, settings.TEST_WEBDRIVER_WAIT_TIMEOUT)
        element = wait.until(EC.invisibility_of_element_located(element))
        return element

    def wait_until_present(self, element):
        wait = WebDriverWait(self.driver, settings.TEST_WEBDRIVER_WAIT_TIMEOUT)
        element = wait.until(EC.presence_of_element_located(element))
        return element

    def wait_until_text_present(self, element, text):
        """
        wait until element is clickable
        """
        wait = WebDriverWait(self.driver, settings.TEST_WEBDRIVER_WAIT_TIMEOUT)
        element = wait.until(EC.text_to_be_present_in_element(element, text))
        return element

    def drag_n_drop(self, object, target):
        """
        used to simulate drag'n drop to move elemens
        from
        http://stackoverflow.com/questions/29381233/how-to-simulate-html5-drag-and-drop-in-selenium-webdriver/29381532#29381532
        object, target : jquery identifiers
        """

        jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"

        # load jQuery helper
        with open("jquery_load_helper.js") as f:
            load_jquery_js = f.read()

        # load drag and drop helper
        with open("drag_and_drop_helper.js") as f:
            drag_and_drop_js = f.read()

        # load jQuery
        self.driver.execute_async_script(load_jquery_js, jquery_url)

        # perform drag&drop
        self.driver.execute_script(
            drag_and_drop_js +
            "$('{}').simulateDragDrop({ dropTarget: '{}'});".format(
                object, target
            )
        )

    def get_url(self, cls):
        """
        return url path of first link inside class element
        """
        el = self.driver.find_element_by_class_name(cls)
        link = el.find_element_by_tag_name('a')
        return link.get_attribute('href')


class StartPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        # prepare driver
        super(StartPage, self).__init__(driver)

        # load page
        if user.operator_set.exists():
            self.operator = user.operator_set.all()[0]
        self.login(username=user.username,
                   password=DEFAULT_TEST_DATA['password'])
        self.get('%s%s' % (live_server_url, '/start/'))

    # --- ACTIONS
    def add_shareholder(self, user):
        el = self.driver.find_element_by_id('add_shareholder')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')

        inputs[0].send_keys(user.first_name)
        inputs[1].send_keys(user.last_name)
        inputs[2].send_keys(user.email)
        inputs[3].send_keys(random.randint(1, 6000))

    def enter_add_company_data(self, *args, **kwargs):
        el = self.driver.find_element_by_id('add_company')
        form = el.find_element_by_tag_name('form')
        inputs = form.find_elements_by_tag_name('input')

        inputs[0].send_keys(DEFAULT_TEST_DATA.get('company_name'))
        self.use_datepicker('add-company')
        inputs[2].send_keys(kwargs.get('count', DEFAULT_TEST_DATA.get('count')))
        inputs[3].send_keys(kwargs.get('value', DEFAULT_TEST_DATA.get('value')))

    def enter_search_term(self, term=None):
        el = self.driver.find_element_by_class_name('search-input')
        el.send_keys(term or 'some term')

    def sort_table_by_number(self):
        selects = self.driver.find_elements_by_tag_name('select')
        select = Select(selects[0])
        select.select_by_visible_text('Gesellschafter Nummer')

    # -- CLICKs
    def click_save_add_company(self):
        el = self.driver.find_element_by_id('add_company')
        el = el.find_element_by_class_name('btn-add-company')
        el.click()

    def click_open_add_shareholder(self):
        time.sleep(2)  # FIXME
        el = self.driver.find_element_by_link_text(
            "Aktionär hinzufügen")
        el.click()

    def click_paginate_next(self):
        btn = self.driver.find_element_by_class_name('paginate-next')
        btn.click()

    def click_save_add_shareholder(self):
        el = self.driver.find_element_by_id('add_shareholder')
        div = el.find_elements_by_class_name('form-group')[1]
        button = div.find_elements_by_tag_name('button')[1]
        button.click()

    def click_search(self):
        el = self.driver.find_element_by_class_name('search-btn')
        el.click()

    # --- GET
    def get_row_by_shareholder(self, shareholder):
        els = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "tr")]')
        for el in els:
            if shareholder.get_full_name() in el.text:
                return el

    def get_total_share_count(self):
        tds = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "totals")]//div[contains(@class, "td")]')
        td = tds[-1]
        return int(td.text.split('(')[0].rstrip())

    def get_company_share_count(self):
        tds = self.driver.find_elements_by_xpath(
            '//div[contains(@class, "totals")]/div[contains(@class, "td")]')
        td = tds[-1]
        return int(td.text)

    # --- CHECKS
    def has_shareholder_count(self):
        return len(self.driver.find_elements_by_xpath(
            '//div[contains(@class, "tr") and contains(@class, "shareholder")]'
        ))

    def is_add_company_form_displayed(self):
        el = self.driver.find_element_by_id('add_company')
        return el.is_displayed()

    def is_properly_displayed(self):
        try:
            assert self._is_element_displayed(id='shareholder_list') is True
            assert self.operator.user.username in self.driver.page_source
            assert self.operator.company.name in self.driver.page_source
            return True
        except AssertionError:
            return False
