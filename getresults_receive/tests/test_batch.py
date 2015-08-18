from datetime import datetime, date

from django.test.testcases import TransactionTestCase
from django.utils import timezone

from getresults_patient.models import Patient

from ..batch_helper import BatchError, BatchHelper

from ..models import Batch, BatchItem, Receive


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
            )
            items.append(batch_item)
        self.assertEqual(BatchItem.objects.all().count(), 0)
        batch_helper = BatchHelper(batch)
        self.assertRaises(BatchError, batch_helper.add, items)
        self.assertEqual(BatchItem.objects.all().count(), 0)

    def test_receive_save_ok(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        for _ in range(3):
            receive = Receive(
                batch=batch,
                patient=patient,
                receive_datetime=datetime.today(),
                collection_date=date.today(),
                collection_time=datetime.today().now(),
                protocol_number='BHP080',
                clinician_initials='XM',
                specimen_condition='10',
                sample_type='WB',
                site_code='02',
                tube_count=1,
            )
            items.append(receive)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 0)
        BatchHelper(batch).savedraft_batch(items)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 3)

    def test_receive_save_raises(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        items = []
        for _ in range(3):
            receive = Receive(
                batch=batch,
            )
            items.append(receive)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 0)
        batch_helper = BatchHelper(batch)
        self.assertRaises(BatchError, batch_helper.savedraft_batch, items)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 0)

    def test_savedraft_batch(self):
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
        BatchHelper(batch).savedraft_batch(items)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 0)
        self.assertEqual(BatchItem.objects.filter(batch=batch).count(), 3)

    def test_savereceive_batch_fail(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        for _ in range(3):
            receive = Receive(
                patient=patient,
            )
            items.append(receive)
        batch_helper = BatchHelper(batch)
        self.assertRaises(BatchError, batch_helper.receive_batch, items)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 0)
        self.assertEqual(BatchItem.objects.filter(batch=batch).count(), 3)

    def test_receivebatch_status_open(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        for _ in range(3):
            receive = Receive(
                patient=patient,
            )
            items.append(receive)
        batch_helper = BatchHelper(batch)
        self.assertRaises(BatchError, batch_helper.receive_batch, items)
        self.assertEqual(batch.status, "Open")
    
    def test_batch_status_closed(self):
        batch = Batch.objects.create(item_count=3, sample_type='WB')
        patient = Patient.objects.create(registration_datetime=timezone.now())
        items = []
        for _ in range(3):
            receive = Receive(
                batch=batch,
                patient=patient,
                receive_datetime=datetime.today(),
                collection_date=date.today(),
                collection_time=datetime.today().now(),
                protocol_number='BHP080',
                clinician_initials='XM',
                specimen_condition='10',
                sample_type='WB',
                site_code='02',
                tube_count=1,
            )
            items.append(receive)
        BatchHelper(batch).receive_batch(items)
        self.assertEqual(batch.status, "Closed")
    
    def test_receive_saveddraft(self):
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
        BatchHelper(batch).savedraft_batch(items)
        receive_items = []
        batch_items = BatchItem.objects.filter(batch=batch)
        for item in batch_items:
            receive = Receive(
                batch=item.batch,
                patient=item.patient,
                specimen_reference=item.specimen_reference,
                receive_datetime=datetime.today(),
                collection_date=date.today(),
                collection_time=datetime.today().now(),
                protocol_number='BHP080',
                clinician_initials='XD',
                specimen_condition='10',
                sample_type='WB',
                site_code='02',
                tube_count=1,
            )
            receive_items.append(receive)
        BatchHelper(batch).receive_batch(receive_items)
        self.assertEqual(Receive.objects.filter(batch=batch).count(), 3)
        self.assertEqual(BatchItem.objects.filter(batch=batch).count(), 0)
