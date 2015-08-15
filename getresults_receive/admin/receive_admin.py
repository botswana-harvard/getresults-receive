from django.contrib import admin

from ..models import Receive

from .getresults_admin import admin_site


class ReceiveAdmin(admin.ModelAdmin):

    date_hierarchy = 'receive_datetime'

    list_display = ('receive_identifier', 'receive_datetime', 'sample_type', 'protocol_number', 'batch_identifier')
    list_filter = ('receive_datetime', 'sample_type', 'protocol_number')
    search_fields = ('receive_datetime', 'protocol_number',)
admin_site.register(Receive, ReceiveAdmin)
