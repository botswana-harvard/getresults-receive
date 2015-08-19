import time

from getresults.tests.base_selenium_test import BaseSeleniumTest

from ..forms import BatchForm


class TestBatchForm(BaseSeleniumTest):

    def setUp(self):
        self.data = {}

    def test_batch_valid(self):
        # create form data
        self.data = dict(batch_identifier='NA', item_count=5, status='done')
        # initial a form
        batch_form = BatchForm(data=self.data)

        # assert form
        self.assertTrue(batch_form.is_valid())

    def test_batch_not_valid(self):
        # create form data
        self.data = dict(batch_identifier=None, item_count=5, status='done')
        # initial a form
        batch_form = BatchForm(data=self.data)

        # assert form
        self.assertFalse(batch_form.is_valid())
