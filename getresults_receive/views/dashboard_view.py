from django.views.generic import TemplateView
from django.conf import settings

from ..models import Receive


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        _project_name = None
        _sections = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name=self.project_name,
            sections=self.sections,
            title="LIMS",
            header=['Patient Identifier', 'Receive Identifier', ' Receive Datetime'],
            header_count=3,
            received=self.received,
            received_count=self.received.count(),
        )
        return context

    @property
    def sections(self):
        """Override in to give a list of sections within the project"""
        return 'Receive'

    @property
    def project_name(self):
        if 'PROJECT_NAME' in dir(settings):
            return settings.PROJECT_NAME
        else:
            return ''

    @property
    def received(self):
        return Receive.objects.filter()
