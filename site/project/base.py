import os
import datetime
import logging
import traceback
import inspect

from django.conf import settings
from django.test import LiveServerTestCase
from django.core.mail import EmailMessage, get_connection

from selenium import webdriver
from pyvirtualdisplay import Display


class BaseSeleniumTestCase(LiveServerTestCase):

    def _screenshot(self):
        # filename = 'screenshot_{}.png'.format(datetime.datetime.now())
        # self.selenium.save_screenshot(filename)
        filename = 'screenshot_{}.png'.format(datetime.datetime.now())
        if not os.path.exists(settings.TEST_ERROR_SCREENSHOTS_DIR):
            os.mkdir(settings.TEST_ERROR_SCREENSHOTS_DIR)
        filepath = os.path.join(
            settings.TEST_ERROR_SCREENSHOTS_DIR, filename)
        self.selenium.save_screenshot(filepath)

        # in test env its using locmem backend
        if settings.TEST_ERROR_SEND_EMAIL:
            caller = inspect.stack()[2][3]
            message = (
                u'FE Test failed. See attached screenshot\n\n'
                u'stacktrace:\n\n%s\n\nbrowser log:\n%s\n\nurl: %s' % (
                    traceback.format_exc(),
                    self.selenium.get_log('browser'),
                    self.selenium.current_url
                )
            )
            email = EmailMessage(
                subject='[darg] FE Test failed w/ %s' % caller,
                body=message,
                from_email='no-reply@das-aktienregister.ch',
                to=('jirka.schaefer@tschitschereengreen.com',),
                connection=get_connection(
                    backend='django.core.mail.backends.smtp.EmailBackend'),
            )

            email.attach_file(filepath)
            email.send()
            print("Email with Screenshot was sent...")

        if not settings.TEST_ERROR_KEEP_SCREENSHOTS:
            os.remove(filepath)

    def _handle_exception(self, e):
        """ on error print JS console of browser and also make a screenshot"""
        # print browser console
        # for entry in self.selenium.get_log('browser'):
        #     print(entry)

        logger = logging.getLogger('tests')

        try:
            logger.error(self.selenium.get_log('browser'))
        except Exception as ex:
            logger.warn(u'Could not get browser log: {}'.format(ex))

        # print python exception
        logger.error(
            u"\nPython Exception: {}\n{}".format(e, traceback.format_exc()))
        # print(u"Python Exception: {}".format(e), traceback.format_exc())

        try:
            self._screenshot()  # make screenshot
        except Exception as ex:
            logger.warn(u'Could not handle debug screenshot: {}'.format(ex))

        # reraise Exc
        raise

    @classmethod
    def setUpClass(cls):
        # debug options
        # options = webdriver.ChromeOptions()
        # options.binary_location = '/usr/bin/google-chrome'
        # service_log_path = "./chromedriver.log"
        # service_args = ['--verbose']

        window_size = (1024, 768)

        # Add following 2 line before start the Chrome
        cls.display = Display(visible=0, size=window_size)
        cls.display.start()

        chrome_options = webdriver.chrome.options.Options()
        chrome_options.add_argument("--start-maximized")
        # avoid TimeoutException https://goo.gl/sSxERk
        # - approach did not work...
        # chrome_options.add_argument('--dns-prefetch-disable')
        cls.selenium = webdriver.Chrome(
            settings.TEST_CHROMEDRIVER_EXECUTABLE,
            chrome_options=chrome_options
        )
        cls.selenium.set_window_size(*window_size)
        # cls.selenium.implicitly_wait(settings.TEST_WEBDRIVER_IMPLICIT_WAIT)

        super(BaseSeleniumTestCase, cls).setUpClass()

        # failed to resolve TimeoutException
        # cls.selenium.set_page_load_timeout(30)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        cls.display.stop()
        super(BaseSeleniumTestCase, cls).tearDownClass()
