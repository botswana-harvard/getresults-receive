from django.db.models import Q

from ..search import BaseSearcher


class AliquotSearch(BaseSearcher):
    """Basic search with patiet identifier """

    def __init__(self):
        self.aliqut_identifier = None
        self.date_received = None
        self.date_drawn = None
        self.patient_identifier = None
        self.protocol = None
        self.q_filter = Q()

    @property
    def search_model(self):
        raise "Not implemented, search_model "

    def search_filter_attributes(self):
        """Search filter in a dictionary format
            Args:
                None
            Returns:
                A Q object with filtering attributes.
        """
        return dict(patient_identifier=self.patient_identifier,
                    date_received=self.date_received,
                    date_drawn=self.date_drawn,
                    protocol=self.protocol)

    @property
    def qset(self):
        """Django Q object containing filtering options
            Args:
                None
            Returns:
                A Q object with filtering attributes.
        """
        self.q_filter.add(Q(aliqout_identifier__icontains=str(self.aliqut_identifier)), Q.OR)
        self.q_filter.add(Q(date_received=self.date_received), Q.OR)
        self.q_filter.add(Q(date_drawn=self.date_drawn), Q.OR)
        self.q_filter.add(Q(protocol__icontains=str(self.protocol)), Q.OR)
        self.q_filter.add(Q(patient_identifier__icontains=str(self.patient_identifier)), Q.OR)
        return self.q_filter


class ReceiveSearch(AliquotSearch):
    pass


class OrderSearch(AliquotSearch):
    pass
