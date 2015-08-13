from django.test.testcases import TestCase
from django.utils import timezone
from django.db import IntegrityError

from getresults_receive.models import Receive, Patient, ReceiveIdentifier, IdentifierHistory


class TestReceive(TestCase):

    @property
    def patient(self):
        patient_identifier = 'P12345678'
        return Patient.objects.create(
            patient_identifier=patient_identifier,
            registration_datetime=timezone.now())

    def test_create(self):
        self.assertIsInstance(Receive.objects.create(
            patient=self.patient), Receive)

    def test_create_identifier(self):
        receive = Receive.objects.create(
            patient=self.patient)
        self.assertEqual(receive.receive_identifier, 'AAA00015')

    def test_update_identifier_history_thru_model(self):
        receive = Receive.objects.create(
            patient=self.patient)
        self.assertEqual(receive.receive_identifier, 'AAA00015')
        self.assertEqual(
            IdentifierHistory.objects.get(identifier=receive.receive_identifier).identifier,
            receive.receive_identifier)

    def test_update_identifier_history(self):
        receive_identifier = ReceiveIdentifier()
        self.assertEqual(
            IdentifierHistory.objects.get(identifier=receive_identifier.identifier).identifier,
            receive_identifier.identifier)

    def test_increment_identifier(self):
        receive = Receive.objects.create(
            patient=self.patient)
        self.assertEqual(receive.receive_identifier, 'AAA00015')
        new = ReceiveIdentifier()
        self.assertEqual(new.identifier, 'AAA00023')
        new = ReceiveIdentifier()
        self.assertEqual(new.identifier, 'AAA00031')
        new = ReceiveIdentifier()
        self.assertEqual(new.identifier, 'AAA00049')
        new = ReceiveIdentifier()
        self.assertEqual(new.identifier, 'AAA00057')
        new = ReceiveIdentifier()
        self.assertEqual(new.identifier, 'AAA00065')

    def test_receive_many(self):
        patient = self.patient
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA00015')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA00023')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA00031')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA00049')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA00057')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA00065')

    def test_receive_identifier_history(self):
        patient = self.patient
        receive = Receive.objects.create(
            patient=patient)
        self.assertIsInstance(
            IdentifierHistory.objects.get(identifier=receive.receive_identifier),
            IdentifierHistory)
        receive = Receive.objects.create(
            patient=patient)
        self.assertIsInstance(
            IdentifierHistory.objects.get(identifier=receive.receive_identifier),
            IdentifierHistory)

    def test_receive_integrity(self):
        patient = self.patient
        receive = Receive.objects.create(
            patient=patient)
        patient = self.patient
        self.assertRaises(
            IntegrityError, Receive.objects.create,
            receive_identifier=receive.receive_identifier,
            patient=patient)

    def test_receive_edit(self):
        patient = self.patient
        receive = Receive.objects.create(
            patient=patient)
        receive_identifier = receive.receive_identifier
        self.assertEqual(receive.receive_identifier, receive_identifier)
        receive.save()
        self.assertIsInstance(
            IdentifierHistory.objects.get(identifier=receive.receive_identifier),
            IdentifierHistory)
        self.assertEqual(receive.receive_identifier, receive_identifier)