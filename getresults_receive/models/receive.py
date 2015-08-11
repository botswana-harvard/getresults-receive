from django.db import models
from django.utils import timezone

from edc_base.model.models import BaseUuidModel, HistoricalRecords
# from edc.base.model.fields import InitialsField
from .identifiers import ReceiveIdentifier
from .patient import Patient


class Receive(BaseUuidModel):

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

    sample_type = models.CharField(
        verbose_name='Sample Type',
        max_length=25,
        choices=(('WB', 'Whole Blood'),
                 ('PL', 'Plasma'),
                 ('BC', 'Buffy Coat'),
                 ('BM', 'Breast milk'),
                 ('ST', 'Stool'), ),
        default='WB')

    protocol_number = models.CharField(
        verbose_name='Protocol Number',
        max_length=6,
        choices=(('cancer', 'BHP045'),
                 ('hnscc', 'BHP065'),
                 ('bcpp', 'BHP066'),
                 ('eit', 'BHP074'), ))

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.receive_identifier, self.receive_datetime.strftime('%Y-%m-%d %H:%M'))

    def save(self, *args, **kwargs):
        if not self.id and not self.receive_identifier:
            self.receive_identifier = ReceiveIdentifier().identifier
        super(Receive, self).save(*args, **kwargs)

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_receive'
