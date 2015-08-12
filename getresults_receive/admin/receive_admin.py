from django.contrib import admin

from ..models import Receive


@admin.register(Receive)
class ReceiveAdmin(admin.ModelAdmin):

    date_hierarchy = 'receive_datetime'

    list_display = ('receive_identifier', 'receive_datetime', 'sample_type', 'protocol_number')
    list_filter = ('receive_datetime', 'sample_type', 'protocol_number')
    search_fields = ('receive_datetime', 'protocol_number')
