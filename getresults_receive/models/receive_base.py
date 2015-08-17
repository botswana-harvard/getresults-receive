from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel

from getresults_patient.models import Patient


class ReceiveBase(BaseUuidModel):

    receive_datetime = models.DateTimeField(
        default=timezone.now)

    collection_datetime = models.DateTimeField(
        default=timezone.now)

    patient = models.ForeignKey(Patient)

    clinician_initials = models.CharField(
        verbose_name='Clinician initials',
        max_length=2,
        default='--', )

    class Meta:
        abstract = True
