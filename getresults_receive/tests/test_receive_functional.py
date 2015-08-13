import time

from django.contrib.auth.models import User

from .base_functional_test import BaseFunctionalTest


class TestReceiveFunctional(BaseFunctionalTest):

    def test_login(self):
        # Only authorized users can access the system
        self.assertEquals(User.objects.all().count(), 1)
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('username').send_keys('rumplestiltskin')
        self.browser.find_element_by_id('password').send_keys('sheepshanks')
        self.browser.find_element_by_id('login').click()
        time.sleep(1)
        self.assertIn('receive', self.browser.title.lower())

    def test_batch_receive_pop(self):
        self.login()
        self.browser.get(self.live_server_url + '/receive')
        self.browser.find_element_by_id('#receiveModal').click()
        time.sleep(5)
        self.switch_to_new_window('Receive', 'myModalLabel')
