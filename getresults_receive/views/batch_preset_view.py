from django.views.generic import TemplateView
from django.shortcuts import render

from ..models import Receive


def show_batch(request, **kwargs):
    batch = Receive.objects.filter(batch_identifier=kwargs.get('batch_identifier'))
    kwargs['batch_received'] = batch
    return BatchPresetView.as_view()(request, **kwargs)


class BatchPresetView(TemplateView):
    template_name = 'receive.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request):
        #form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request):
        #form = self.form_class(initial=self.initial)
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            sections_head='Receive Batch',
            title="Receive Batch",
            batch_size=range(1, 5),
        )
        return context