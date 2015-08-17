from django.db import models

from edc_base.model.models import BaseUuidModel

from .batch import Batch
from .receive_base import ReceiveBase


class BatchItem(ReceiveBase):

    batch = models.ForeignKey(Batch)

    class Meta:
        app_label = "getresults_receive"
