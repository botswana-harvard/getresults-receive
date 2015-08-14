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
        self.browser.find_element_by_id('batchbutton').click()
        time.sleep(1)
        self.switch_to_new_window('Receive', 'batchModalLabel')

    def test_receive_batch_pops_up(self):
        self.test_login()
        self.browser.get('http://localhost:8000/receive/')
        receive_batch_button = self.browser.find_element_by_id('receive_batch_button')
        receive_batch_button.click()
        time.sleep(1)
        self.switch_to_new_window('Receive Sample', 'receive_button_id')

    def test_autofill_sample_type(self):
        self.fail('finish test')

    def test_autofill_protocol_number(self):
        self.fail('finish test')

    def test_dynamically_change_receive_form_rows(self):
        self.fail('finish test')