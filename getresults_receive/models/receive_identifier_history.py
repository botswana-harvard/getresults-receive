from django.db import models
from django.utils import timezone


class ReceiveIdentifierHistory(models.Model):

    identifier = models.CharField(
        max_length=16,
        null=True,
        editable=False,
    )

    alpha = models.CharField(
        max_length=10,
    )

    numeric = models.IntegerField(
        null=True)

    allocated = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_receiveidentifier'
        ordering = ('identifier', 'numeric', )
