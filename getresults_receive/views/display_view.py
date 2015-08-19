from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ..models import Batch, BatchItem


def display_batch(request, **kwargs):
    batch = Batch.objects.filter(user_created=request.user.username)
    # batch = Batch.objects.all()
    kwargs['batches'] = batch
    kwargs['header'] = [
        'Batch Identifier',
        'Item Count',
        'Status',
        'Protocol Number',
        'Site Code'
    ]
    kwargs['template_name'] = 'my_batch.html'
    return DisplayView.as_view()(request, **kwargs)


def show_batch(request, **kwargs):
    batch = BatchItem.objects.filter(batch__batch_identifier=kwargs.get('batch_identifier'))
    kwargs['batch_received'] = batch
    kwargs['header'] = [
        'Patient',
        'Receive Datetime',
        'Specimen Reference',
        'Protocol Number',
        'Specimen Condition',
        'Sample Type'
    ]
    kwargs['template_name'] = 'batch_items.html'
    return DisplayView.as_view()(request, **kwargs)


class Option(object):

    def __init__(self, link_text, href, data_toggle, data_target):
        self.link_text = link_text
        self.href = href
        self.data_toggle = data_toggle
        self.data_target = data_target
        self.name = self.link_text.lower().replace(' ', '_')


class DisplayView(TemplateView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DisplayView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.template_name = kwargs.get('template_name')
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            project_name='GETRESULTS: RECEIVE',
            section_head="",
            title='GETRESULTS RECEIVE',
            sidebar_options=[
                Option('Receive by batch', None, 'modal', '#batchModal'),
                Option('Receive single', None, 'modal', '#sampleModal'),
                Option('View my batches', 'receive_user_batches', None, None),
                Option('View all batches', '#', None, None),
                Option('Search for batch', '#', None, None),
                Option('Search for specimen', '#', None, None),
            ],
            batches=kwargs.get('batches'),
            batch_received=kwargs.get('batch_received')
        )
        return context
