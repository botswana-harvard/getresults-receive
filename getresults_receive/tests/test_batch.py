import random

from datetime import datetime

from django.test.testcases import TransactionTestCase
from django.utils import timezone

from getresults_patient.models import Patient
from ..exceptions import BatchError
from ..models import Batch, BatchItem, Receive
from getresults_receive.constants import OPEN, RECEIVED, SAVED
from getresults_receive.exceptions import AlreadyReceivedError, BatchDuplicateItemError, BatchSaveError


class TestBatch(TransactionTestCase):

    def setUp(self):
        self.batch = Batch.objects.create(
            item_count=3,
            specimen_condition='OK',
            specimen_type='WB')
        self.patient = Patient.objects.create(registration_datetime=timezone.now())

    def random_string(self, length):
        return ''.join([random.choice('ABCDEFGHIJKLMNOPQRTUVWZYZ123456789') for _ in range(length)])

    def new_batch_item_instance(self, batch=None, patient=None, collection_datetime=None):
        return BatchItem(
            batch=batch or self.batch,
            patient=patient or self.patient,
            protocol_number='BHP000',
            clinician_initials='MM',
            specimen_condition='OK',
            collection_datetime=collection_datetime or timezone.now(),
            tube_count=1,
        )

    def test_create_batch_identifier(self):
        """Test that a batch identifier is assigned when batch created"""
        prefix = datetime.today().strftime('%Y%m%d')
        self.assertTrue(self.batch.batch_identifier.startswith(prefix))

    def test_update_batch_no_change_identifier(self):
        """Test that a batch identifier does not change on update"""
        batch_id = self.batch.batch_identifier
        self.batch.save()
        self.assertEqual(batch_id, self.batch.batch_identifier)

    def test_batchitem_duplicate_raises(self):
        batch = self.batch
        batch.item_count = 2
        items = []
        collection_datetime = timezone.now()
        items.append(self.new_batch_item_instance(batch, collection_datetime=collection_datetime))
        items.append(self.new_batch_item_instance(batch, collection_datetime=collection_datetime))
        self.assertRaises(BatchSaveError, self.batch.save_batch_items, items)

    def test_batchitem_count_raises(self):
        items = []
        batch = self.batch
        for _ in range(4):
            batch_item = self.new_batch_item_instance(batch)
            items.append(batch_item)
        self.assertEqual(BatchItem.objects.all().count(), 0)
        self.assertRaises(BatchError, batch.save_batch_items, items)
        self.assertEqual(BatchItem.objects.all().count(), 0)

    def test_batch_receive_save(self):
        items = []
        batch = self.batch
        for _ in range(3):
            items.append(self.new_batch_item_instance(batch))
        batch.save_batch_items(items)
        self.assertEqual(BatchItem.objects.filter(batch=self.batch).count(), 3)
        batch.receive_batch_items()
        receive_identifiers = batch.get_receive_identifiers()
        self.assertEqual(Receive.objects.filter(receive_identifier__in=receive_identifiers).count(), 3)

    def test_save_batch(self):
        items = []
        batch = self.batch
        for _ in range(3):
            items.append(self.new_batch_item_instance(batch))
        batch.save_batch_items(items)
        self.assertEqual(BatchItem.objects.filter(batch=self.batch).count(), 3)

    def test_save_batch_already_received(self):
        batch = self.batch
        batch.status = RECEIVED
        batch.save()
        items = []
        for _ in range(3):
            items.append(self.new_batch_item_instance(batch))
        self.assertRaises(AlreadyReceivedError, batch.save_batch_items, items)

    def test_batch_status_open(self):
        batch = self.batch
        self.assertEqual(batch.status, OPEN)
        items = []
        for _ in range(3):
            items.append(self.new_batch_item_instance(batch))
        batch.save_batch_items(items)
        self.assertEqual(self.batch.status, SAVED)

    def test_batch_status_received(self):
        items = []
        batch = self.batch
        for _ in range(3):
            items.append(self.new_batch_item_instance())
        batch.save_batch_items(items)
        batch.receive_batch_items()
        self.assertEqual(batch.status, RECEIVED)
