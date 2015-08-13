import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.test import LiveServerTestCase


class TestReceiveFunctional(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        User.objects.create_superuser('rumplestiltskin', 'django@bhp.org.bw', 'sheepshanks')

    def tearDown(self):
        self.browser.quit()

    def login(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('username').send_keys('rumplestiltskin')
        self.browser.find_element_by_id('password').send_keys('sheepshanks' + Keys.RETURN)

    def test_login(self):
        # Only authorized users can access the system
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('username').send_keys('rumplestiltskin')
        self.browser.find_element_by_id('password').send_keys('sheepshanks')
        self.browser.find_element_by_id('login').click()
        self.assertIn('receive', self.browser.title.lower())

    def test_batch_receive_pop(self):
        self.login()
        self.browser.get(self.live_server_url + '/receive')
        self.browser.find_element_by_id('#receiveModal').click()
        time.sleep(5)
        self.switch_to_new_window('Receive', 'myModalLabel')
