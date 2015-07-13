from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from .patient import Patient
from .receive_identifier import ReceiveIdentifier
from .receive_identifier_history import ReceiveIdentifierHistory


class Receive(BaseUuidModel):

    receive_identifier = models.CharField(
        max_length=25,
        unique=True)

    receive_datetime = models.DateTimeField(
        default=timezone.now())

    patient = models.ForeignKey(Patient)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.receive_identifier, self.receive_datetime.strftime('%Y-%m-%d %H:%M'))

    def save(self, *args, **kwargs):
        if not self.id and not self.receive_identifier:
            try:
                receive_identifier_history = ReceiveIdentifierHistory.objects.latest('id')
                last_identifier = receive_identifier_history.identifier
            except ReceiveIdentifierHistory.DoesNotExist:
                last_identifier = None
            identifier = ReceiveIdentifier(last_identifier)
            self.receive_identifier = identifier.identifier
            ReceiveIdentifierHistory.objects.create(identifier=self.receive_identifier)
        super(Receive, self).save(*args, **kwargs)

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_receive'
