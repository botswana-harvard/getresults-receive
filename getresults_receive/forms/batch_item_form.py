from django.forms import ModelForm
from django import forms

from ..models import BatchItem


class BatchItemForm(forms.ModelForm):

    receive_datetime = forms.DateField(required=False)
    collection_date = forms.DateField(required=False)
    collection_time = forms.TimeField(required=False)
    protocol_number = forms.CharField(max_length=6, required=False)
    site_code = forms.CharField(max_length=2, required=False)

    class Meta:
        model = BatchItem
        fields = ['batch', 'patient']
