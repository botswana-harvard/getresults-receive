from django.db import models
from django.utils import timezone
from django.apps import apps
from django.db import IntegrityError, transaction

from edc_base.model.models import BaseUuidModel
from getresults_identifier.batch_identifier import BatchIdentifier

from ..constants import SAVED, OPEN, RECEIVED
from ..exceptions import BatchError, BatchReceiveError, BatchSaveError, AlreadyReceivedError

from .receive import ReceiveBaseFieldsMixin, Receive


class Batch(ReceiveBaseFieldsMixin, BaseUuidModel):

    batch_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
    )

    batch_datetime = models.DateTimeField(
        default=timezone.now,
        editable=False,
    )

    status = models.CharField(
        max_length=10,
        default=OPEN,
        editable=False,
    )

    item_count = models.IntegerField(
        default=1,
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.batch_identifier = BatchIdentifier().identifier
        super().save(*args, **kwargs)

    def save_batch_items(self, batch_items):
        """Saves the items to the BatchItem model or does a rollback and
        raises an exception."""
        if self.status == RECEIVED:
            raise AlreadyReceivedError(
                'Batch {} is already received.'.format(self.batch_identifier))
        if len(batch_items) != self.item_count:
            raise BatchError(
                'Expected {} items. Got {}'.format(self.item_count, len(batch_items)))
        try:
            with transaction.atomic():
                for batch_item in batch_items:
                    batch_item.save()
            self.status = SAVED
            self.modified = timezone.now()
            self.save(update_fields=['status', 'modified'])
        except IntegrityError as e:
            raise BatchSaveError(str(e))

    def receive_batch_items(self):
        """Saves batch to the Receive model or raises an exception."""
        BatchItem = apps.get_model(self._meta.app_label, 'BatchItem')
        if self.status == RECEIVED:
            raise AlreadyReceivedError('Batch {} is already received.'.format(self.batch_identifier))
        elif self.status == OPEN:
            raise BatchSaveError('Batch {} has not been saved.'.format(self.batch_identifier))
        elif self.status == SAVED:
            try:
                with transaction.atomic():
                    for batch_item in BatchItem.objects.filter(batch=self):
                        receive = Receive.objects.create(
                            patient=batch_item.patient,
                            collection_datetime=batch_item.collection_datetime,
                            specimen_type=batch_item.specimen_type,
                            specimen_reference=batch_item.specimen_reference,
                            receive_datetime=timezone.now(),
                            protocol_number=batch_item.protocol_number,
                            clinician_initials=batch_item.clinician_initials,
                            specimen_condition=batch_item.specimen_condition,
                            site_code=batch_item.site_code,
                            tube_count=batch_item.tube_count,
                        )
                        batch_item.receive_identifier = receive.receive_identifier
                        batch_item.save()
                self.status = RECEIVED
                self.save()
            except IntegrityError as e:
                raise BatchReceiveError(str(e))
        else:
            raise BatchError('Unknown status for batch {}. Got {}'.format(self, self.status))

    def get_receive_identifiers(self):
        BatchItem = apps.get_model(self._meta.app_label, 'BatchItem')
        return [batch_item.receive_identifier for batch_item in BatchItem.objects.filter(batch=self)]

    class Meta:
        app_label = "getresults_receive"
