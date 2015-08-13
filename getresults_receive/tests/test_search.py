from django.test.testcases import TestCase
from django.db.models import Q

from .factories import PatientFactory
from ..models import Patient
from ..search import BaseSearcher


class PatientSearch(BaseSearcher):
    """Basic search with patiet identifier """

    def __init__(self, patient_identifier=None, protocol=None):
        super(PatientSearch, self).__init__()
        self.patient_identifier = patient_identifier
        self.protocol = protocol
        self.q_filter = Q()

    @property
    def search_model(self):
        return Patient

    @property
    def search_filter_attributes(self):
        return dict(patient_identifier=self.patient_identifier,
                    protocol=self.protocol,
                    )

    @property
    def qset(self):
        """Django Q object containing filtering options
            Args:
                None
            Returns:
                A Q object with filtering attributes.
        """
        self.q_filter.add(Q(patient_identifier__icontains=str(self.patient_identifier)), Q.OR)
        self.q_filter.add(Q(protocol__contains=str(self.protocol)), Q.OR)
        return self.q_filter


class TestSearch(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        Patient.objects.all().delete()

    def test_basic_search(self):
        """Test search by full patient identifier"""
        patient = PatientFactory()

        self.assertEqual(1, PatientSearch(patient_identifier=patient.patient_identifier, protocol='LIS').basic_search.count())

    def test_basic_search_with_multiple(self):
        """Test search by full patient identifier"""
        patient = PatientFactory()
        multiple_fields = dict(patient_identifier=patient.patient_identifier, protocol='LIS')
        self.assertEqual(1, PatientSearch(**multiple_fields).basic_search.count())

    def test_basic_extended(self):
        """Search for all records matching a substring of patient identifier. """
        for _ in range(5):
            PatientFactory()
        self.assertEqual(5, PatientSearch(patient_identifier='21444678').extended_search.count())

    def test_basic_extended_invalid(self):
        """Search for records with no matching string."""
        for _ in range(5):
            PatientFactory()
        self.assertEqual(0, PatientSearch(patient_identifier='7570055X', protocol='tsetsiba').extended_search.count())

    def test_basic_extended_invalid1(self):
        """ """
        for _ in range(5):
            PatientFactory()
        self.assertEqual(0, PatientSearch(patient_identifier='21444678BBC').extended_search.count())

    def test_search_by_full_identifier(self):
        """Test search by full patient identifier"""
        patient = PatientFactory()

        self.assertEqual(1, PatientSearch(patient_identifier=patient.patient_identifier).search_result.count())

    def test_search_by_part_of_identifier(self):
        """Test search by substring of patient identifier"""
        PatientFactory()

        self.assertEqual(1, PatientSearch(patient_identifier='21444678').search_result.count())

    def test_search_view_aliquout(self):
        """ """
        pass

    def test_search_view_ordering(self):
        """ """
        pass

    def test_search_view_receiving(self):
        """ """
        pass
