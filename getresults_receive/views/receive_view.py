from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ..models import Receive, Batch

from getresults_patient.models import Patient

from ..forms import BatchItemForm
from ..models import BatchItem
from ..batch_helper import BatchHelper, BatchError


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
        named_template = 'receive_batch_items.html'
        context = self.get_context_data(named_template=named_template)
        if (request.GET.get('action') and (request.GET.get('action') == ('receive' or 'draft'))):

            if request.POST.get('action') == 'receive':
                batch_items_list = self.batch_items_list_post(request)
                if not self.validate_batch_items(batch_items_list):
                    named_template = 'receive_batch_items.html'
                    forms = self.batch_item_form_list(batch_items_list)
                    context.update(batch_item_forms=forms)
                    context.update(batch_item_status=True)
                    context.update(batch_preset=False)
                else:
                    self.save_valid_batch_items(request.POST.get('patient_identifier'),
                                                self.batch_items_list_post(request))
                    context.update(named_template=named_template)
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
            batch_present=False,
            received=Receive.objects.all(),
            received_count=Receive.objects.all().count(),
            is_batch_item_valid=False,
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

    def field_data(self, index, request, field):
        field_data = request.POST.getlist(field, None)
        return field_data[index] if field_data else None

    def batch_items_list_post(self, request):
        batch_items_list = []
        for i in range(len(request.POST.getlist('patient_name', []))):
            form_field = ['patient_name', 'collect_datetime', 'rec_datetime_name', 'sample_type_name',
                          'protocol_no_name', 'site_code_name']
            _batch_items_list = []
            for field in form_field:
                _batch_items_list.append(self.field_data(i, request, field))
            batch_items_list.append(dict(patient=_batch_items_list[0], collection_datetime=_batch_items_list[1],
                                         receive_datetime=_batch_items_list[2], sample_type=_batch_items_list[3],
                                         protocol_number=_batch_items_list[4], site_code=_batch_items_list[5])
                                    )
        return batch_items_list

    def batch_items(self, batch_items_list):
        """ """
        batch_items = []
        for batch_item_data in batch_items_list:
            batch_item_data.update({'patient': self.patient(batch_item_data.get('patient'))})
            batch_item = BatchItem.objects.build(**batch_item_data)
            batch_items.append(batch_item)
        return batch_items

    def save_valid_batch_items(self, batch_identifier, batch_items_list):
        batch_helper = BatchHelper(self.batch(batch_identifier))
        message = "{} Batch items successfully added".format(len(batch_items_list))
        try:
            batch_helper.receive_batch(batch_items_list)
        except BatchError as message:
            return message
        return message

    def patient(self, patient_identifier):
        try:
            patient = Patient.objects.get(patient_identifier=patient_identifier)
        except Patient.DoesNotExist:
            pass
        return patient

    def batch_item_form_list(self, batch_items_list):
        batch_items_forms = []
        for batch_item_data in batch_items_list:
            batch_item_form = BatchItemForm(data=batch_item_data)
            batch_items_forms.append(batch_item_form)
        return batch_items_forms

    def validate_batch_items(self, batch_items_list):
        for batch_item_form in self.batch_item_form_list(batch_items_list):
            if not batch_item_form.is_valid():
                return False
        return True

    def batch(self, batch_identifier):
        batch = None
        try:
            batch = Batch.objects.get(batch_identifier=batch_identifier)
        except Batch.DoesNotExist:
            return Batch.objects.first()  # for development purpose only.
        return batch
