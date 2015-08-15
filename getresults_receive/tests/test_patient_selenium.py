import time

from .base_selenium_test import BaseSeleniumTest


class TestPatientSelenium(BaseSeleniumTest):
    username = 'melissa'
    password = '123'
    email = 'm@123.org'

    def navigate_to_admin_receive_patient(self):
        self.navigate_to_admin()
        self.login()
        self.navigate_to_admin_getresults_receive()
        time.sleep(2)
        element = self.browser.find_element_by_link_text('Patients')
        element.click()

    def test_patient_required_fields(self):
        self.navigate_to_admin_receive_patient()
        time.sleep(1)
        element = self.browser.find_element_by_link_text('Add patient')
        element.click()

    def test_can_create_patient_via_admin(self):
        '''User goes to browser and access the admin page'''
        self.navigate_to_admin_receive_patient()
        time.sleep(2)
        element = self.browser.find_element_by_link_text('Add patient')
        element.click()
        time.sleep(1)
        # Now nurse needs to add details for this patient
        patient_id = self.browser.find_element_by_name('patient_identifier')
        patient_id.send_keys('065-910099-1')
        protocol_no = self.browser.find_element_by_name('protocol')
        protocol_no.send_keys('BHP065')
        acc = self.browser.find_element_by_name('account')
        acc.send_keys('BHP065')
        reg_date = self.browser.find_element_by_name('registration_datetime')
        reg_date.send_keys('2015/08/14 03:30')
        gender = self.browser.find_element_by_css_selector("input[value='F']")
        gender.click()
        dob = self.browser.find_element_by_name('dob')
        dob.send_keys('1995/08/14')
        omang_id = self.browser.find_element_by_name('identity')
        omang_id.send_keys('111121111')
        save_button = self.browser.find_element_by_css_selector("input[type='submit']")
        save_button.click()
        time.sleep(1)
