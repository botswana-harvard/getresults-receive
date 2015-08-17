from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel

from getresults_patient.models import Patient

from ..choices import PROTOCOL


class ReceiveBase(BaseUuidModel):

    receive_identifier = models.CharField(
        max_length=25,
        editable=False,
        unique=True, )

    receive_datetime = models.DateTimeField(
        default=timezone.now)

    collection_datetime = models.DateTimeField(
        default=timezone.now)

    patient = models.ForeignKey(Patient)

    clinician_initials = models.CharField(
        verbose_name='Clinician initials',
        max_length=2,
        default='--', )

    protocol_number = models.CharField(
        verbose_name='Protocol Number',
        max_length=6,
        choices=PROTOCOL)


    class Meta:
        abstract = True
