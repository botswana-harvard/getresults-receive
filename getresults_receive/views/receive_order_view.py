from django.views.generic import TemplateView
from django.conf import settings
from _datetime import datetime


class ReceiveOrderView(TemplateView):
    template_name = 'receive_order.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name=self.project_name(),
            sections_head='Receive Order',
            sections=self.sections(),
            title="Receive Order",
            header=['', 'Patient Identifier', 'Received Datetime', 'Order 1', 'Order 2'],
            labels={'Add': 'Receive new samples', 'View': 'View Received samples', 'Remove': 'Remove received samples'},
            aliquots=[n for n in range(0, 10)],
            received_count=10,
            received_date=str(datetime.now())
        )
        return context

    def sections(self):
        """Override in to give a list of sections within the project"""
        return ['Order by Date Received', ' Received by User', 'View All Received']

    def project_name(self):
        if 'PROJECT_NAME' in dir(settings):
            return settings.PROJECT_NAME
        else:
            return ''
