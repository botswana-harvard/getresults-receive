from django.views.generic import TemplateView

from ..forms import BatchForm


class BatchPresetView(TemplateView):
    template_name = 'receive.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, request, **kwargs):
        context = self.get_context_data()
        context.update(named_template='receive_batch_items.html')
        return self.render_to_response(context)

    def post(self, request):
        context = self.get_context_data()
        form = BatchForm(request.POST)
        if form.is_valid():
            item_count = form.cleaned_data.get('item_count')
            collection_date = form.cleaned_data.get('collection_date')
            sample_type = form.cleaned_data.get('sample_type')
            protocol_no = form.cleaned_data.get('protocol_no')
            site_code = form.cleaned_data.get('site_code')
            context.update(collection_date_name=collection_date.strftime("%Y-%m-%d") if collection_date else '',
                           sample_type_name=sample_type,
                           protocol_no_name=protocol_no,
                           site_code_name=site_code,
                           batch_size=range(0, item_count),
                           named_template='receive_batch_items.html'
                           )
            return self.render_to_response(context)
        else:
            raise 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            sections_head='Receive Batch',
            title="Receive Batch",
            batch_size=range(0, 5),
        )
        return context
