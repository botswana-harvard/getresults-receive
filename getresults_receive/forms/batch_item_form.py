from django.forms import ModelForm
from ..models import BatchItem


class BatchItemForm(ModelForm):

    class Meta:
        model = BatchItem
        fields = ['batch']
