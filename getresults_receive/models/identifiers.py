from getresults_identifier import AlphanumericIdentifier

from .identifier_history import IdentifierHistory


class PatientIdentifier(AlphanumericIdentifier):

    identifier_type = 'patient'
    alpha_pattern = r'^[A-Z]{3}$'
    numeric_pattern = r'^[0-9]{8}$'
    seed = ['AAA', '00000000']
    history_model = IdentifierHistory


class ReceiveIdentifier(AlphanumericIdentifier):

    identifier_type = 'receive'
    alpha_pattern = r'^[A-Z]{3}$'
    numeric_pattern = r'^[0-9]{4}$'
    seed = ['AAA', '0000']
    history_model = IdentifierHistory
