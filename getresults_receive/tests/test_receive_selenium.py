import time

from .base_selenium_test import BaseSeleniumTest


class TestReceiveSelenium(BaseSeleniumTest):

    def test_open_receive(self):
        '''Asserts user can open receive sample window'''
        self.login()
        self.assertTrue('Receive', self.browser.title)
        self.browser.save_screenshot('getresults_receive/snapshots/receive.png')

    def test_open_receive_sample_modal(self):
        '''Asserts user can open receive sample window'''
        self.login()
        self.assertTrue('Receive', self.browser.title)
        sample_button = self.browser.find_element_by_name("receive_sample")
        sample_button.click()
        time.sleep(1)
        self.browser.save_screenshot('getresults_receive/snapshots/receive_sample.png')

    def test_open_receive_batch_modal(self):
        '''Asserts user can open receive sample window'''
        self.login()
        self.assertTrue('Receive', self.browser.title)
        sample_button = self.browser.find_element_by_name("receive_batch")
        sample_button.click()
        time.sleep(1)
        self.browser.save_screenshot('getresults_receive/snapshots/receive_batch.png')


#     def test_autofill_sample_type(self):
#         self.fail('finish test')
# 
#     def test_autofill_protocol_number(self):
#         self.fail('finish test')
# 
#     def test_dynamically_change_receive_form_rows(self):
#         self.fail('finish test')
