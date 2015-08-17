from django.views.generic import TemplateView

from ..models import Receive


def show_batch(request, **kwargs):
    batch = Receive.objects.filter(batch_identifier=kwargs.get('batch_identifier'))
    kwargs['batch_received'] = batch
    return BatchPresetView.as_view()(request, **kwargs)


class BatchPresetView(TemplateView):
    template_name = 'reveive.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            sections_head='Receive Batch',
            title="Receive Batch",
            header=[
                'Batch Identifier',
                'Patient Identifier',
                'Receive Identifier',
                'Collection Datetime',
                'Receive Datetime',
                'Sample Type',
                'Protocol Number',
            ],
            batch=kwargs['batch_received'],
        )
        return context