from django.db import models

from edc_base.model.models import BaseUuidModel

from .batch import Batch


class BatchItems(BaseUuidModel):
    
    batch = models.ForeignKey(Batch)
    
    class Meta:
        app_label = "batch_items"
