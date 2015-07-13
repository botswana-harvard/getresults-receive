from django.test.testcases import TestCase

from getresults_receive.models import Receive


class TestReceive(TestCase):

    def test_create(self):
        Receive.objects.create()
