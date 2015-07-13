from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from ..receive_identifier import ReceiveIdentifier

from .receive_identifier_history import ReceiveIdentifierHistory
from .receive import Receive


@receiver(pre_save, weak=False, dispatch_uid='receive_identifier_on_presave')
def receive_identifier_on_presave(sender, instance, raw, using, **kwargs):
    if not raw:
        if isinstance(instance, Receive):
            if not instance.id:
                try:
                    receive_identifier_history = ReceiveIdentifierHistory.objects.latest('id')
                    last_identifier = receive_identifier_history.identifier
                except ReceiveIdentifierHistory.DoesNotExist:
                    last_identifier = None
                identifier = ReceiveIdentifier(last_identifier)
                instance.receive_identifier = identifier.identifier
