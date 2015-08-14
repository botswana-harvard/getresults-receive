# from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base_functional_test import BaseFunctionalTest


class TestReceiveSampleFunctional(BaseFunctionalTest):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_user_can_login(self):
        '''User goes to browser to access login page'''
        self.browser.get(self.live_server_url)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Please sign in', body.text)
        username = self.browser.find_element_by_name('username')
        username.send_keys('rumplestiltskin')
        userpwd = self.browser.find_element_by_name('password')
        userpwd.send_keys('sheepshanks')
        # userpwd.send_keys(Keys.RETURN)
        self.browser.find_element_by_name('login').click()
        # we're logged in, inspect where you are
        self.assertTrue('Receive', self.browser.title)
        # click on the receive sample button
        sample_button = self.browser.find_element_by_css_selector("button.btn.btn-primary.btn-lg")
        if sample_button.text == "Receive Sample":
            sample_button.click()
        self.fail("I still have more testing to do")
