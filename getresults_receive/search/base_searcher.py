from datetime import date, time, datetime, timedelta

from django.db import models
from builtins import ValueError


class SearchError(Exception):
    pass


class BaseSearcher(object):

    """ Base search class. """

    search_model = None
    order_by = ['-modified', '-created']

    def __init__(self, search_filter_values=None):
        self.search_filter_values = search_filter_values

    @property
    def search_model(self):
        """Model the system will query.
            Args:
                None
            Returns:
                 A model instance.
        """
        raise NotImplementedError("The method should be implemented in sub class.")

    @property
    def qset(self):
        """Django Q object containing filtering options
            Args:
                None
            Returns:
                A Q object with filtering attributes.
        """
        raise NotImplementedError("The method should be implemented in sub class.")

    def determine_field_type(self, field, qset):
        model_field = self.search_model._meta.get_field(field)
        if isinstance(model_field, models.CharField):
            pass
        else:
            pass

    @property
    def search_filter_attributes(self):
        """Search filter attributes (key/pair).
            Args:
                None
            Returns:
                A list of dictionary with attributes to search with. e.g [dict(attrib=1), dict()..]
        """
        raise NotImplementedError("The method should be implemented in sub class.")

    @property
    def basic_search(self):
        """Do a simple search on a particular model
            Args:
                None
            Returns:
                Search results
        """
        return self.search_model.objects.filter(**self.search_filter_attributes).order_by(*self.order_by)

    @property
    def extended_search(self):
        """Do a extended search on a particular model
            Args:
                None
            Returns:
                Search results
        """
        return self.search_model.objects.filter(self.qset).order_by(*self.order_by)

    @property
    def search_result(self):
        """Determines the result of a search with more results. """
        extended_count = 0
        basic_count = 0
        try:
            extended_count = self.extended_search.count()
        except ValueError:
            try:
                basic_count = self.basic_search.count()
            except ValueError:
                pass
        if extended_count > basic_count:
            return self.extended_search
        return self.basic_search

    @property
    def search_value(self):
        pass

    @property
    def special_keyword_queryset(self):

        if self.search_value.lower() == '?':
            queryset = self.search_model.objects.all().order_by('-modified')[0:15]
        elif self.search_value.lower().startswith('?last'):
            limit = self.search_value.lower().split('?last')[1] or 15
            queryset = self.search_model.objects.all().order_by('-modified')[0:limit]
        elif self.search_value.lower().startswith('?first'):
            limit = self.search_value.lower().split('?first')[1] or 15
            queryset = self.search_model.objects.all().order_by('modified')[0:limit]
        elif self.search_value.lower() == '?today':
            queryset = self.search_model.objects.filter(modified__gte=datetime.combine(date.today(), time.min)).order_by('modified')
        elif self.search_value.lower() == '?yesterday':
            queryset = self.search_model.objects.filter(
                modified__gte=datetime.combine(date.today() - timedelta(days=1), time.min)).order_by('modified')
        elif self.search_value.lower() == '?lastweek':
            queryset = self.search_model.objects.filter(
                modified__gte=datetime.combine(date.today() - timedelta(days=7), time.min)).order_by('modified')
        else:
            queryset = None
        return queryset
