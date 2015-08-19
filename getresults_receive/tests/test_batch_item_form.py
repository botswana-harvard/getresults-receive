from django.utils import timezone
from datetime import datetime
from django.test.testcases import TestCase

from getresults_patient.tests.factories import PatientFactory

from ..views import ReceiveView
from ..forms import BatchItemForm
from ..models import Batch, BatchItem


class TestBatchItemForm(TestCase):

    def setUp(self):
        self.data = {}
        self.batch_items = []

    def test_batch_items(self):
        pass

    def test_batch_item_valid(self):
        patient = PatientFactory()
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        batch_items = dict(patient=patient.id, batch=batch.id)

        batch_item_form = BatchItemForm(data=batch_items)

        self.assertTrue(batch_item_form.is_valid())

    def test_batch_item_valid_with_all(self):
        patient = PatientFactory()
        batch = Batch.objects.create(item_count=3, sample_type='WB', )
        batch_items = dict(protocol_number='bhp066', patient=patient.id, batch=batch.id, collection_date=timezone.now(),
                           sample_type='WB', colection_time=timezone.now())
        batch_item_form = BatchItemForm(data=batch_items)
        print(batch_item_form.data)
        for row in batch_item_form.fields.values(): print(row)
        self.assertTrue(batch_item_form.is_valid())

    def test_batch_not_valid_without_batch(self):
        patient = PatientFactory()
        batch_items = dict(patient=patient.id, colection_time=timezone.now(), collection_date=timezone.now(), sample_type='WB',
                           protocol_number='bhp06688')

        batch_item_form = BatchItemForm(data=batch_items)

        self.assertFalse(batch_item_form.is_valid())

    def test_batch_not_valid_without_batch1(self):
        patient = PatientFactory()
        batch_items = dict(patient=patient.id, colection_time=timezone.now(), collection_date=timezone.now(), sample_type='WB',
                           protocol_number='bhp06688')

        batch_item_form = BatchItemForm(data=batch_items)

        self.assertIn('batch', batch_item_form.errors)

    def test_batch_item_form_list(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = PatientFactory()
        receive = ReceiveView()
        batch_item_form_list = [dict(protocol_number='bhp066', patient=patient.id, batch=batch.id, collection_date=timezone.now(),
                                     sample_type='WB', colection_time=timezone.now())
                                ]
        self.assertEqual(len(receive.batch_item_form_list(batch_item_form_list)), 1)

    def test_batch_item_form(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = PatientFactory()
        receive = ReceiveView()
        batch_item_form_list = [dict(protocol_number='bhp066', patient=patient.id, batch=batch.id, collection_date=timezone.now(),
                                     sample_type='WB', colection_time=timezone.now())
                                ]
        self.assertTrue(receive.validate_batch_items(batch_item_form_list))

    def test_batch(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = PatientFactory()
        receive = ReceiveView()
        batch_item_form_list = [dict(protocol_number='bhp066', patient=patient.id, batch=batch.id, collection_date=timezone.now(),
                                     sample_type='WB', colection_time=timezone.now())
                                ]
        self.assertTrue(receive.batch(batch.batch_identifier))
