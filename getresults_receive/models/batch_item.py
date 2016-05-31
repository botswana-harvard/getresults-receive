from django.db import models

from edc_base.model.models import BaseUuidModel

from getresults_patient.models import Patient

from .batch import Batch
from .receive import ReceiveBaseFieldsMixin


class BatchItem(ReceiveBaseFieldsMixin, BaseUuidModel):

    batch = models.ForeignKey(Batch)

    patient = models.ForeignKey(Patient)

    collection_datetime = models.DateTimeField()

    clinician_initials = models.CharField(
        verbose_name='Clinician\'s initials',
        max_length=3,
        null=True,
        blank=True,
    )

    specimen_reference = models.CharField(max_length=25, null=True, blank=True)

    tube_count = models.IntegerField()

    receive_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    class Meta:
        app_label = "getresults_receive"
        unique_together = ('batch', 'patient', 'collection_datetime', 'specimen_type')
