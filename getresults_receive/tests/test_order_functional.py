#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import time
import unittest
from selenium import webdriver
from getresults_aliquot.models import Aliquot
from getresults_aliquot.tests.factories import AliquotFactory


class TestOrderFunctional(unittest.TestCase):
    server_url = 'http://localhost:8000/'

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.server_url + "receive_order/")
        time.sleep(3)
        self.create_aliquots(20)

    def tearDown(self):
#         self.browser.get(self.server_url+"?testing=remove")
        self.browser.quit()

    def test_correct_page(self):
        self.assertIn('Receive Order', self.browser.title)

    def test_order_popup_button(self):
        order_button = self.browser.find_element_by_id('order-{}'.format(Aliquot.objects.all()[0].aliquot_identifier))
        order_button.click()
        time.sleep(2)
        self.switch_to_new_window('Order against aliquot', 'myModalLabel')

    def test_submit_order_popup(self):
        order_button = self.browser.find_element_by_id('order-button-0')
        order_button.click()
        time.sleep(2)
        self.switch_to_new_window('Order against aliquot', 'myModalLabel')
        submit_button = self.browser.find_element_by_id('order-submit')
        submit_button.submit()
        time.sleep(3)
        self.assertIn('Receive Order', self.browser.title)

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

#     def create_aliquots(self, number):
#         for n in range(1, number):
#             AliquotFactory()
