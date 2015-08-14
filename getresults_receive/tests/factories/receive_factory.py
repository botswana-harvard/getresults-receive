import factory

from datetime import datetime

from getresults_receive.models import Receive


class ReceiveFactory(factory.DjangoModelFactory):
    class Meta:
        model = Receive

    receive_identifier = factory.Sequence(lambda n: 'APA{0}K-{0}'.format(n))
    receive_datetime = datetime.today()
    collection_datetime = datetime.today()
    patient = factory.Sequence(lambda n: '099-21444678-{0}'.format(n))
    clinician_initials = 'DD'
    sample_type = 'WB'
    protocol_number = 'BHHRL'
    batch_identifier = factory.Sequence(lambda n: 'XXHT-{0}'.format(n))
