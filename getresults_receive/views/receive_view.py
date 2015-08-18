from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import render

from ..models import Receive
from ..models import Batch


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
            # For post requests, the template we will include depends on what the user is attempting to do.
            named_template = 'receive_batch_items.html'
        context = self.get_context_data(named_template=named_template)
        return self.render_to_response(context)

    def get(self, request):
        # For get requests, its safe to assume the user will always be trying to receive a batch
        named_template = 'receive_batch_items.html'
        context = self.get_context_data(named_template=named_template)
        return self.render_to_response(context)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ReceiveView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        username = self.request.user.username
        context = super().get_context_data(**kwargs)
        context.update(
            project_name='GETRESULTS: RECEIVE',
            section_name="RECEIVE",
            title='GETRESULTS RECEIVE',
            sidebar_options=[
                Option('Receive by batch', None, 'modal', '#batchModal'),
                Option('Receive single', None, 'modal', '#sampleModal'),
                Option('View my batches', 'receive_user_batches', None, None),
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

#     def get(self, request):
#         batch = Batch.objects.filter(user_created=request.user.username)
#         context = self.get_context_data()
#         context.update(
#             batch,
#             header=[
#                 'Batch Identifier',
#                 'Item Count',
#                 'Status',
#                 'Protocol Number',
#                 'Site Code'
#             ],
#             named_template='my_batch.html'
#         )
#         return self.render_to_response(context)
