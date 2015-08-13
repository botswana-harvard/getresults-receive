import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class BaseFunctionalTest(LiveServerTestCase):

    def setUp(self):
        super().setUp()
        try:
            self.browser = webdriver.Chrome()
        except AttributeError:
            self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('username').send_keys('rumplestiltskin')
        self.browser.find_element_by_id('password').send_keys('sheepshanks' + Keys.RETURN)

    def switch_to_new_window(self, text_in_element, element_id):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                element = self.browser.find_element_by_id(element_id)
                if text_in_element in element.text:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find pop-up window')
