from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from getresults_patient.models import Patient

from .batch import Batch
from .identifiers import ReceiveIdentifier


class Receive(BaseUuidModel):

    receive_identifier = models.CharField(
        max_length=25,
        editable=False,
        unique=True
    )

    batch = models.ForeignKey(Batch)

    patient = models.ForeignKey(Patient)

    receive_datetime = models.DateTimeField(
        default=timezone.now
    )

    specimen_reference = models.CharField(
        max_length=25)

    collection_date = models.DateField()

    collection_time = models.TimeField()

    protocol_number = models.CharField(
        verbose_name='Protocol',
        max_length=6,
    )

    clinician_initials = models.CharField(
        verbose_name='Clinician\'s initials',
        max_length=3,
    )

    specimen_condition = models.IntegerField()

    sample_type = models.CharField(
        max_length=2,
    )

    site_code = models.CharField(
        max_length=2,
        null=True,
        blank=True,
    )

    tube_count = models.IntegerField()

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(
            self.receive_identifier, self.receive_datetime.strftime('%Y-%m-%d %H:%M'))

    def save(self, *args, **kwargs):
        if not self.id and not self.receive_identifier:
            self.receive_identifier = ReceiveIdentifier().identifier
        super(Receive, self).save(*args, **kwargs)

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_receive'
