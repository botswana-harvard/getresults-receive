from django.test.testcases import TestCase
from django.utils import timezone
from django.db import IntegrityError

from getresults_receive.models import Receive, Patient, ReceiveIdentifier, ReceiveIdentifierHistory


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
        self.assertEqual(receive.receive_identifier, 'AAA0001')

    def test_increment_identifier(self):
        receive = Receive.objects.create(
            patient=self.patient)
        self.assertEqual(receive.receive_identifier, 'AAA0001')
        new = ReceiveIdentifier(receive.receive_identifier)
        self.assertEqual(new.identifier, 'AAA0002')
        new = ReceiveIdentifier(new.identifier)
        self.assertEqual(new.identifier, 'AAA0003')
        new = ReceiveIdentifier(new.identifier)
        self.assertEqual(new.identifier, 'AAA0004')
        new = ReceiveIdentifier(new.identifier)
        self.assertEqual(new.identifier, 'AAA0005')
        new = ReceiveIdentifier(new.identifier)
        self.assertEqual(new.identifier, 'AAA0006')

    def test_receive_many(self):
        patient = self.patient
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA0001')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA0002')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA0003')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA0004')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA0005')
        receive = Receive.objects.create(
            patient=patient)
        self.assertEqual(receive.receive_identifier, 'AAA0006')

    def test_receive_identifier_history(self):
        patient = self.patient
        receive = Receive.objects.create(
            patient=patient)
        self.assertIsInstance(
            ReceiveIdentifierHistory.objects.get(identifier=receive.receive_identifier),
            ReceiveIdentifierHistory)
        receive = Receive.objects.create(
            patient=patient)
        self.assertIsInstance(
            ReceiveIdentifierHistory.objects.get(identifier=receive.receive_identifier),
            ReceiveIdentifierHistory)

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
            ReceiveIdentifierHistory.objects.get(identifier=receive.receive_identifier),
            ReceiveIdentifierHistory)
        self.assertEqual(receive.receive_identifier, receive_identifier)
