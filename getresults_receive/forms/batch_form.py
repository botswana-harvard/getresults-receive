from django import forms

from ..models import Batch


class BatchForm(forms.ModelForm):

    item_count = forms.IntegerField(required=True)
    collection_datetime = forms.DateTimeField(required=False)
    specimen_type = forms.CharField(max_length=5, required=False)
    protocol_number = forms.CharField(max_length=5, required=False)
    site_code = forms.CharField(max_length=2, required=False)

    class Meta:
        model = Batch
        fields = ['item_count']
