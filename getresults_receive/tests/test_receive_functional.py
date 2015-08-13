from django.contrib.auth.models import User
from selenium import webdriver

from .base_functional_test import BaseFunctionalTest


class TestReceiveFunctional(BaseFunctionalTest):

    def setUp(self):
        try:
            self.browser = webdriver.Chrome()
        except AttributeError:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        User.objects.create_superuser('rumplestiltskin', 'django@bhp.org.bw', 'sheepshanks')

    def tearDown(self):
        self.browser.implicitly_wait(30)
        self.browser.quit()

    def test_login(self):
        # Only authorized users can access the system
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('username').send_keys('rumplestiltskin')
        self.browser.find_element_by_id('password').send_keys('sheepshanks')
        self.browser.find_element_by_id('login').click()
        self.assertIn('receive', self.browser.title.lower())
