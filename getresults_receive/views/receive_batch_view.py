from django.views.generic import TemplateView
from django.conf import settings

from ..models import Receive


class ReceiveBatchView(TemplateView):
    template_name = 'receive_batch.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name=self.project_name(),
            sections_head='Receive Batch',
            title="Receive Batch",
            # header=['Patient Identifier', 'Receive Identifier', 'Collection Datetime', 'Receive Datetime', 'Sample Type', 'Protocol Number'],
            # labels={'Add': 'Receive new samples', 'View': 'View Received samples', 'Remove': 'Remove received samples'},
            # header_count=3,
            batch_range_to_receive=range(10),
            # received=self.received(),
            # received_count=self.received().count(),
        )
        return context

    def project_name(self):
        if 'PROJECT_NAME' in dir(settings):
            return settings.PROJECT_NAME
        else:
            return ''

#     def received(self):
#         return Receive.objects.filter()
