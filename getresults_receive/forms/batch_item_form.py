from django.forms import ModelForm
from ..models import BatchItems


class BatchItemForm(ModelForm):

    class Meta:
        model = BatchItems
        fields = ['batch']
