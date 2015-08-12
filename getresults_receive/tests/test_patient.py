from django.test.testcases import TestCase
from django.utils import timezone

from getresults_receive.models import Patient


class TestPatient(TestCase):

    def test_create(self):
        self.assertIsInstance(Patient.objects.create(
            patient_identifier='P12345678',
            registration_datetime=timezone.now()),
            Patient
        )
