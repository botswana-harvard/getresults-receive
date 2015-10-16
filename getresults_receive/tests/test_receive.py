from django.test.testcases import TestCase
from django.utils import timezone
from django.db import IntegrityError

from getresults_patient.models import Patient
from getresults_receive.models import Receive, Batch
from getresults_identifier.models import IdentifierHistory


class TestReceive(TestCase):

    def setUp(self):
        patient_identifier = 'P12345678'
        self.patient = Patient.objects.create(
            patient_identifier=patient_identifier,
            registration_datetime=timezone.now()
        )
        self.batch = Batch.objects.create()
        self.receive = Receive.objects.create(
            patient=self.patient,
            tube_count=1,
            specimen_condition='10',
            collection_datetime=timezone.now())

    def test_creates_identifier(self):
        self.assertEqual(self.receive.receive_identifier, 'AAA00015')

    def test_updates_identifier_history_thru_model(self):
        self.assertEqual(self.receive.receive_identifier, 'AAA00015')
        self.assertEqual(
            IdentifierHistory.objects.get(identifier=self.receive.receive_identifier).identifier,
            self.receive.receive_identifier)

    def test_receive_many(self):
        self.assertEqual(self.receive.receive_identifier, 'AAA00015')
        receive = Receive.objects.create(
            patient=self.patient,
            specimen_condition='10',
            tube_count=1,
            collection_datetime=timezone.now())
        self.assertEqual(receive.receive_identifier, 'AAA00023')
        receive = Receive.objects.create(
            patient=self.patient,
            tube_count=1,
            specimen_condition='10',
            collection_datetime=timezone.now())
        self.assertEqual(receive.receive_identifier, 'AAA00031')
        receive = Receive.objects.create(
            patient=self.patient,
            tube_count=1,
            specimen_condition='10',
            collection_datetime=timezone.now())
        self.assertEqual(receive.receive_identifier, 'AAA00049')
        receive = Receive.objects.create(
            patient=self.patient,
            tube_count=1,
            specimen_condition='10',
            collection_datetime=timezone.now())
        self.assertEqual(receive.receive_identifier, 'AAA00057')
        receive = Receive.objects.create(
            patient=self.patient,
            tube_count=1,
            specimen_condition='10',
            collection_datetime=timezone.now())
        self.assertEqual(receive.receive_identifier, 'AAA00065')

    def test_receive_identifier_history(self):
        self.assertIsInstance(
            IdentifierHistory.objects.get(identifier=self.receive.receive_identifier),
            IdentifierHistory)
        receive = Receive.objects.create(
            patient=self.patient,
            tube_count=1,
            specimen_condition='10',
            collection_datetime=timezone.now())
        self.assertIsInstance(
            IdentifierHistory.objects.get(identifier=receive.receive_identifier),
            IdentifierHistory)

    def test_receive_integrity(self):
        self.assertRaises(
            IntegrityError, Receive.objects.create,
            receive_identifier=self.receive.receive_identifier,
            patient=self.patient,
            collection_datetime=timezone.now())

    def test_receive_edit(self):
        receive_identifier = self.receive.receive_identifier
        self.assertEqual(self.receive.receive_identifier, receive_identifier)
        self.receive.save()
        self.assertIsInstance(
            IdentifierHistory.objects.get(identifier=self.receive.receive_identifier),
            IdentifierHistory)
        self.assertEqual(self.receive.receive_identifier, receive_identifier)
