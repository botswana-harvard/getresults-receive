from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.conf import settings

from ..models import Receive


class Option(object):

    def __init__(self, link_text, href, data_toggle, data_target):
        self.link_text = link_text
        self.href = href
        self.data_toggle = data_toggle
        self.data_target = data_target
        self.name = self.link_text.lower().replace(' ', '_')


class ReceiveView(TemplateView):

    template_name = 'receive.html'

    def post(self, request):
        named_template = None
        if (request.GET.get('action') and (request.GET.get('action') == ('receive' or 'draft'))):
            named_template = 'receive_batch_items.html'
        context = self.get_context_data(named_template=named_template)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReceiveView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name='GETRESULTS: RECEIVE',
            section_name="RECEIVE",
            title='GETRESULTS RECEIVE',
            sidebar_options=[
                Option('Receive by batch', None, 'modal', '#batchModal'),
                Option('Receive single', None, 'modal', '#sampleModal'),
                Option('View my batches', '#', None, None),
                Option('View all batches', '#', None, None),
                Option('Search for batch', '#', None, None),
                Option('Search for specimen', '#', None, None),
            ],
            header=[
                'Identifier',
                'Patient',
                'Collected',
                'Received',
                'Type',
                'Protocol',
                'Batch'
            ],
            labels={
                'Add': 'Receive new samples',
                'View': 'View Received samples',
                'Remove': 'Remove received samples'},
            header_count=3,
            range_to_receive=range(10),
            received=Receive.objects.all(),
            received_count=Receive.objects.all().count()
        )
        return context
