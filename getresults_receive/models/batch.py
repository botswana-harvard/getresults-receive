from django.db import models

from edc_base.model.models import BaseUuidModel
from getresults_identifier.batch_identifier import BatchIdentifier


class Batch(BaseUuidModel):

    batch_identifier = models.CharField(
        max_length=25,
    )

    item_count = models.IntegerField(
        default=1,
    )

    status = models.CharField(
        max_length=10,
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.batch_identifier = BatchIdentifier().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = "batch"
