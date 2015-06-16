from django.db import models

from .patient import Patient

from edc_base.model.models import BaseUuidModel, HistoricalRecords


class Receive(BaseUuidModel):

    receive_identifier = models.CharField(
        max_length=25)

    receive_datetime = models.DateTimeField()

    patient = models.ForeignKey(Patient)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.receive_identifier, self.receive_datetime.strftime('%Y-%m-%d %H:%M'))

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_receive'
