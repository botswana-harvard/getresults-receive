from django.test.testcases import TestCase
from datetime import datetime

from ..models import Batch
  

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

    def test_batch_creates_items(self):
        batch = Batch.objects.create()
        batch_item = BatchItem.objects.filter(batch_idenitifier=batch.batch_identifier)
        self.assertIsNotNone(batch_item)
    