from getresults_identifier import AlphanumericIdentifier


class ReceiveIdentifier(AlphanumericIdentifier):

    alpha_pattern = r'^[A-Z]{3}$'
    numeric_pattern = r'^[0-9]{4}$'
    SEED = ('AAA', '0000')
