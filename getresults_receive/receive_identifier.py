from getresults_identifier import AlphanumericIdentifier

from .models import ReceiveIdentifierHistory


class ReceiveIdentifier(AlphanumericIdentifier):

    alpha_pattern = r'^[A-Z]{3}$'
    numeric_pattern = r'^[0-9]{4}$'
    SEED = ('AAA', '0000')

    def increment(self):
        super(ReceiveIdentifier, self).increment()
        ReceiveIdentifierHistory.objects.create(identifier=self.identifier)
