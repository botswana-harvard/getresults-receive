from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime

class TestProcessFunctional(LiveServerTestCase):

    def setUp(self):
        User.objects.create_superuser('melissa', '', '123')
        super().setUp()
        self.browser = webdriver.Firefox()
        # 3secs timeout when performing actions
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_patient_via_admin(self):
        '''User goes to browser and access the admin page'''
        self.browser.get(self.live_server_url + '/admin/')
        # Selenium inspects whole page and looks for "Django admin..."
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)
        # Now she has to login
        # provide username
        username = self.browser.find_element_by_name('username')
        username.send_keys('melissa')
        # provide password
        userpwd = self.browser.find_element_by_name('password')
        userpwd.send_keys('123')
        userpwd.send_keys(Keys.RETURN)
        # Look for the patient link
        patient_link = self.browser.find_elements_by_css_selector("a[href*='/admin/getresults_receive/patient/']")
        for p in range(0, len(patient_link)):
            link = self.browser.find_elements_by_css_selector("a[href*='/admin/getresults_receive/patient/']")
            link[0].click()
        # Now nurse has to go to the Add Patient Button
        self.browser.find_element_by_link_text('Add patient').click()
        # There are several fields to key in
        inputboxes = self.browser.find_element_by_tag_name('body')
        self.assertTrue('Patient identifier', inputboxes.text)
        self.assertTrue('Protocol', inputboxes.text)
        self.assertIn('Registration datetime', inputboxes.text)
        self.assertIn('Gender', inputboxes.text)
        self.assertIn('Dob', inputboxes.text)
        self.assertIn('Identity', inputboxes.text)
        # Now nurse needs to add details for this patient
        patient_id = self.browser.find_element_by_name('patient_identifier')
        patient_id.send_keys('065-910099-1')
        protocol_no = self.browser.find_element_by_name('protocol')
        protocol_no.send_keys('BHP065')
        acc = self.browser.find_element_by_name('account')
        acc.send_keys('BHP065')
        reg_date = self.browser.find_element_by_name('registration_datetime_0')
        reg_date.send_keys('2015-08-14')
        reg_time = self.browser.find_element_by_name('registration_datetime_1')
        reg_time.send_keys('10:40:52')
        gender = self.browser.find_element_by_id('id_gender')
        if gender.text == 'Female':
            gender.click()
        dob = self.browser.find_element_by_name('dob')
        dob.send_keys('1995-08-14')
        omang_id = self.browser.find_element_by_name('identity')
        omang_id.send_keys('111121111')
        save_button = self.browser.find_element_by_css_selector("input[type='submit']")
        save_button.click()
        self.browser.close()

        # TO DO: still to write more. next step receive
        # TO DO: split this quote into several methods
