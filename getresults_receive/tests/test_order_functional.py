#from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class TestOrderFunctional(unittest.TestCase):
    server_url = 'http://localhost:8000/'

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.browser.get(self.server_url+"receive_order/")

    def tearDown(self):
#         self.browser.get(self.server_url+"?testing=remove")
        self.browser.quit()

    def test_correct_page(self):
        self.assertIn('Receive Order', self.browser.title)
