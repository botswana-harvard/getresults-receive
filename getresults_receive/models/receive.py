from django.db import models

from edc_base.model.models import HistoricalRecords

from .identifiers import ReceiveIdentifier
from .receive_base import ReceiveBase


class Receive(ReceiveBase):
    receive_identifier = models.CharField(
        max_length=25,
        editable=False,
        unique=True, )

    batch_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        editable=False,
    )

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
