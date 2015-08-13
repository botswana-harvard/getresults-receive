from django.views.generic import TemplateView
from django.conf import settings

from ..models import Receive


class ReceiveView(TemplateView):
    template_name = 'receive.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name=self.project_name(),
            sections_head='Receive',
            sections=self.sections(),
            title="Receive",
            header=['Patient Identifier', 'Receive Identifier', 'Collection Datetime', 'Receive Datetime', 'Sample Type', 'Protocol Number', 'Primary Aliquot?'],
            labels={'Add': 'Receive new samples', 'View': 'View Received samples', 'Remove': 'Remove received samples'},
            header_count=3,
            received=self.received(),
            range_to_receive=range(10),
            received_count=self.received().count(),
        )
        return context

    def sections(self):
        """Override in to give a list of sections within the project"""
        return ['Order by Date Received', 'Order by Protocol', 'Order by Sample Type', 'Received by User', 'View All Received']

    def project_name(self):
        if 'PROJECT_NAME' in dir(settings):
            return settings.PROJECT_NAME
        else:
            return ''

    def received(self):
        return Receive.objects.all()
