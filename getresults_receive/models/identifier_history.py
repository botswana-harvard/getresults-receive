from django.db import models

from getresults_identifier.models import BaseIdentifierHistory


class IdentifierHistory(BaseIdentifierHistory):

    alpha = models.CharField(
        max_length=10,
        null=True
    )

    numeric = models.IntegerField(
        null=True)

    class Meta:
        app_label = 'getresults_receive'
        db_table = 'getresults_receiveidentifier'
        ordering = ('identifier', 'numeric', )
