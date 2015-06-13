from django.db import models

from edc_base.model.models import BaseUuidModel
from edc_constants.choices import GENDER


class Patient(BaseUuidModel):

    patient_identifier = models.CharField(
        max_length=25)

    protocol = models.CharField(
        max_length=25,
        null=True)

    account = models.CharField(
        max_length=25,
        null=True)

    registration_datetime = models.DateTimeField()

    gender = models.CharField(
        max_length=10,
        choices=GENDER,
        null=True)

    dob = models.DateField(
        null=True)

    identity = models.CharField(
        max_length=25,
        null=True)

    def __str__(self):
        return self.patient_identifier

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_patient'
