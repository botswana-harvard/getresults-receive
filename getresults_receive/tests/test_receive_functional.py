import unittest
from selenium import webdriver
from django.contrib.auth.models import User


class TestReceiveFunctional(unittest.TestCase):
    site_url = 'http://localhost:8000/'

    def setUp(self):
        self.browser = webdriver.Firefox()
        User.objects.create_superuser('rumplestiltskin', 'django@bhp.org.bw', 'sheepshanks')

    def tearDown(self):
        self.browser.implicitly_wait(30)
        self.browser.quit()

    def test_login(self):
        # Only authorized users can access the system
        self.browser.get(self.site_url)
        self.browser.find_element_by_id('username').send_keys('rumplestiltskin')
        self.browser.find_element_by_id('password').send_keys('sheepshanks')
        self.browser.find_element_by_id('login').click()
        self.assertIn('receive', self.browser.title.lower())
