from getresults_identifier import AlphanumericIdentifier

from getresults.models import IdentifierHistory


class ReceiveIdentifier(AlphanumericIdentifier):

    identifier_type = 'receive'
    alpha_pattern = r'^[A-Z]{3}$'
    numeric_pattern = r'^[0-9]{4}$'
    seed = ['AAA', '0000']
    history_model = IdentifierHistory
