import factory

from getresults_receive.models import Receive
from django.utils import timezone


class ReceiveFactory(factory.DjangoModelFactory):
    class Meta:
        model = Receive

    receive_identifier = factory.Sequence(lambda n: 'APA{0}K-{0}'.format(n))
    receive_datetime = timezone.now()
    collection_datetime = timezone.now()
    patient = factory.Sequence(lambda n: '099-21444678-{0}'.format(n))
    clinician_initials = 'DD'
    specimen_type = 'WB'
    protocol_number = 'BHHRL'
    batch_identifier = factory.Sequence(lambda n: 'XXHT-{0}'.format(n))
    specimen_reference = factory.Sequence(lambda n: 'MMA{0}K-{0}'.format(n))
    site_code = '02'
    tube_count = 1
