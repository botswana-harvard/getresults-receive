from django.db import models

from edc_base.model.models import BaseUuidModel
from getresults_identifier.batch_identifier import BatchIdentifier

from .receive import BaseReceive


class Batch(BaseUuidModel):

    batch_identifier = models.CharField(
        max_length=25,
    )

    item_count = models.IntegerField(
        default=1,
    )

    status = models.CharField(
        max_length=10,
        default='Open',
    )

    sample_type = models.CharField(
        max_length=2,
    )

    protocol_number = models.CharField(max_length=5, null=True, blank=True)

    site_code = models.CharField(max_length=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.batch_identifier = BatchIdentifier().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = "getresults_receive"


class BatchItem(BaseReceive):

    batch = models.ForeignKey(Batch)

    class Meta:
        app_label = "getresults_receive"
