from ...models import Patient
import factory

from datetime import datetime, date
from dateutil import relativedelta

from edc_constants.choices import GENDER


class PatientFactory(factory.DjangoModelFactory):

    FACTORY_FOR = Patient

    patient_identifier = factory.Sequence(lambda n: '066-21444678-{0}'.format(n))
    protocol = 'LIS'
    registration_datetime = datetime.today()

    gender = GENDER[0]

    dob = date.today() - relativedelta(years=25)

    identity = '31791851{0}'
