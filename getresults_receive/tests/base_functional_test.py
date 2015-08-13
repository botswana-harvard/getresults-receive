import time
import unittest
from selenium import webdriver


class BaseFunctionalBase(unittest.TestCase):
    server_url = 'http://localhost:8000/'
    browser = webdriver.Chrome()

    def setUp(self):
        self.browser.get(self.server_url)
        time.sleep(3)

    def tearDown(self):
#         self.browser.get(self.server_url+"?testing=remove")
        self.browser.quit()

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