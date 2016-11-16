"""
learned from here
http://selenium-python.readthedocs.org/en/latest/page-objects.html
"""

# from element import BasePageElement (save all locators here)
# from locators import MainPageLocators (save all setter/getter here)

from django.core.urlresolvers import reverse

from selenium.webdriver.common.by import By

from project.page import BasePage
from project.generators import DEFAULT_TEST_DATA


class CompanyPage(BasePage):
    """Options List View"""

    def __init__(self, driver, live_server_url, user, company):
        """ load MainPage '/' """
        self.live_server_url = live_server_url
        self.company = company

        # prepare driver
        super(CompanyPage, self).__init__(driver)

        # load page
        self.operator = user.operator_set.all()[0]
        self.login(username=user.username,
                   password=DEFAULT_TEST_DATA['password'])
        self.driver.get('%s%s' % (live_server_url, reverse(
            "company", kwargs={'company_id': self.company.pk}
        )))

    # -- INPUT COMMANDs
    def enter_new_operator_email(self, email):
        el = self.driver.find_element_by_id('add-operator-form')
        form = el.find_element_by_tag_name('form')
        field = form.find_element_by_tag_name('input')

        field.send_keys(email)

    def enter_string(self, css_class, string):
        el = self.driver.find_element_by_class_name(css_class)
        el = el.find_element_by_tag_name('input')
        el.send_keys(string)

    # -- CLICKs
    def click_save_new_operator(self):
        # wait for form
        self.wait_until_visible((By.CSS_SELECTOR, '#add-operator-form'))
        el = self.driver.find_element_by_id('add-operator-form')
        button = el.find_element_by_class_name(
            "btn-focus")
        button.click()

    def click_open_add_new_operator_form(self):
        button = self.driver.find_element_by_class_name(
            'toggle-add-operator-form')
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();", button)
        button.click()

    def click_remove_operator(self, operator):
        table = self.driver.find_element_by_class_name(
            'operators'
        )
        self.driver.execute_script(
            "return arguments[0].scrollIntoView();", table)
        rows = table.find_elements_by_tag_name('tr')
        match = False
        for row in rows:
            tds = row.find_elements_by_tag_name('td')
            for td in tds:
                if operator.user.email in td.text:
                    match = True
            if match:
                button = row.find_element_by_class_name('remove-operator')
                button.click()
                break

    def click_to_edit(self, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-click')
        self.scroll_to(element=el)
        el.click()

    def click_open_datepicker(self, class_name):
        """
        click to open the datepicker for element X
        """
        el = self.driver.find_element_by_class_name(class_name)
        btn = el.find_element_by_xpath(
            '//td[@class="date-field"]//span[@class="input-group-btn"]//button'
        )
        self.scroll_to(element=btn)
        btn.click()

    def click_date_in_datepicker(self, class_name):
        """
        select some date in datepicker

        click first day of current month
        """
        el = self.driver.find_element_by_class_name(class_name)
        dp_row = el.find_element_by_xpath(
            '//table[@class="uib-daypicker"]//tr[@class="uib-weeks ng-scope"]')
        for td in dp_row.find_elements_by_tag_name('td'):
            el2 = td.find_elements_by_tag_name('span')
            if el2 and el2[0].text == '01':
                btn = td.find_element_by_tag_name('button')
                btn.click()
                break

    def save_edit(self, class_name):
        el = self.driver.find_element_by_class_name(class_name)
        el = el.find_element_by_class_name('editable-buttons')
        el = el.find_element_by_tag_name('button')
        el.click()

    # -- VALIDATIONs
    def is_operator_displayed(self, email):
        return email in self.driver.page_source

    # --- GET DATA
    def get_founding_date(self, class_name="birthday"):
        """
        return date from inside this element
        """
        bday = self.driver.find_element_by_xpath(
            '//tr[@class="founding-date active"]/td/span')
        return bday.text
