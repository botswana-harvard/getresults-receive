from django.test.testcases import TestCase
from datetime import datetime

from ..utils import BatchHelper

from ..models import Batch, BatchItem


class TestBatch(TestCase):
    
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
    
#     def test_batchitem_save(self):
#         """Test that transaction persists change if no fail"""
#         batch = Batch.objects.create(item_count=3, sample_type='WB')
#         items = []
#         items.append(BatchItem(batch=batch), )
#         items.append(BatchItem(batch=batch))
#         items.append(BatchItem(batch=batch))
#         self.assertEqual(BatchItem.objects.all().count(), 0)
#         BatchHelper().batchitem_transaction(items)
#         self.assertEqual(BatchItem.objects.all().count(), 3)
    
#     def test_batchitem_rollback(self):
#         """Test that transaction rolls back when one item fails"""
#         
#         batch = Batch.objects.create()
#         items = []
#         items.append(BatchItem(batch=batch))
#         items.append(BatchItem(batch=batch))
#         items.append(BatchItem(batch=batch))
#         BatchHelper().batchitem_transaction(items)
#         self.assertEqual(BatchItem.objects.all().count(), 3)
