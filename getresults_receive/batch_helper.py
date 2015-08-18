from django.db import IntegrityError, transaction

from .models import BatchItem


class BatchError(Exception):
    pass


class BatchHelper(object):

    def __init__(self, batch):
        self.batch = batch

    def add(self, items):
        self.validate_count(items)
        try:
            with transaction.atomic():
                for item in items:
                    item.save()
        except IntegrityError as e:
            raise BatchError(str(e))

    def validate_count(self, items):
        if len(items) != self.batch.item_count:
            raise BatchError('Expected {} items. Got {}'.format(self.batch.item_count, len(items)))

    def savedraft_batch(self, items):
        self.add(items)
        self.batch.status = 'Open'
        self.batch.save()

    def receive_batch(self, items):
        try:
            self.add(items)
            self.batch.status = 'Closed'
            self.batch.save()
        except BatchError:
            batch_items = []
            for item in items:
                batch_item = BatchItem(
                    batch=self.batch,
                    patient=item.patient,
                    receive_datetime=item.receive_datetime,
                    specimen_reference=item.receive_datetime,
                    collection_date=item.collection_date,
                    collection_time=item.collection_time,
                    protocol_number=item.protocol_number,
                    clinician_initials=item.clinician_initials,
                    specimen_condition=item.specimen_condition,
                    sample_type=item.sample_type,
                    site_code=item.site_code,
                    tube_count=item.tube_count,
                )
                batch_items.append(batch_item)
            self.savedraft_batch(batch_items)
