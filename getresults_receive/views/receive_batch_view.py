from django.views.generic import TemplateView
from django.conf import settings

from ..choices import SAMPLE_TYPE, PROTOCOL


class ReceiveBatchView(TemplateView):
    template_name = 'receive_batch.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name=self.project_name(),
            choices_procotol=self.choices_procotol(),
            choices_samples=self.choices_samples(),
            sections_head='Receive Batch',
            title="Receive Batch",
            range_to_receive=range(10), )
        return context

    def project_name(self):
        if 'PROJECT_NAME' in dir(settings):
            return settings.PROJECT_NAME
        else:
            return ''

    def choices_procotol(self):
        choices_list = []
        for item in PROTOCOL:
            choices_list.append(item[1])
        return choices_list

    def choices_samples(self):
        samples_list = []
        for s in SAMPLE_TYPE:
            samples_list.append(s[1])
        return samples_list
