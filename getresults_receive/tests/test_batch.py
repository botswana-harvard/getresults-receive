from datetime import datetime

from django.test.testcases import TransactionTestCase
from django.utils import timezone

from getresults_patient.models import Patient

from ..models import Batch, BatchItem

from ..batch_helper import BatchError, BatchHelper
from getresults_receive.models.receive import Receive


class TestBatch(TransactionTestCase):

    def test_create_batch(self):
        """Test that a batch identifier is assigned when batch created"""
        batch = Batch.objects.create()
        prefix = datetime.today().strftime('%Y%m%d')
        self.assertTrue(batch.batch_identifier.startswith(prefix))

    def test_update_batch_identifier(self):
        """Test that a batch identifier is unique"""
        batch = Batch.objects.create()
        batch_id = batch.batch_identifier
        batch.save()
        self.assertEqual(batch_id, batch.batch_identifier)

    def test_batchitem_count_raises(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        items.append(BatchItem(batch=batch, patient=patient))
        items.append(BatchItem(batch=batch, patient=patient))
        batch_helper = BatchHelper(batch)
        self.assertRaises(BatchError, batch_helper.add, items)

    def test_batchitem_count(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        items.append(BatchItem(batch=batch, patient=patient))
        items.append(BatchItem(batch=batch, patient=patient))
        batch_helper = BatchHelper(batch)
        self.assertRaises(BatchError, batch_helper.add, items)

    def test_batchitem_save_raises(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        items = []
        for _ in range(3):
            batch_item = BatchItem(
                batch=batch,
            )
            items.append(batch_item)
        self.assertEqual(BatchItem.objects.all().count(), 0)
        batch_helper = BatchHelper(batch)
        self.assertRaises(BatchError, batch_helper.add, items)
        self.assertEqual(BatchItem.objects.all().count(), 0)

    def test_batchitem_save_ok(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        for n in range(3):
            batch_item = BatchItem(
                batch=batch,
                patient=patient,
                specimen_reference=str(n),
            )
            items.append(batch_item)
        self.assertEqual(BatchItem.objects.filter(batch=batch).count(), 0)
        batch_helper = BatchHelper(batch)
        batch_helper.add(items)
        self.assertEqual(BatchItem.objects.filter(batch=batch).count(), 3)    

    def test_savedraft_sample(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        for n in range(3):
            batch_item = BatchItem(
                batch=batch,
                patient=patient,
                specimen_reference=str(n),
            )
            items.append(batch_item)
        batch_helper = BatchHelper(batch).savedraft_batch(items)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 0)
        self.assertGreater(BatchItem.objects.filter(batch=batch).count(), 0)
