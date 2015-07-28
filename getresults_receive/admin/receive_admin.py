from django.contrib import admin

from ..models import Receive


@admin.register(Receive)
class ReceiveAdmin(admin.ModelAdmin):

    date_hierarchy = 'receive_datetime'

    list_display = ('receive_identifier', 'receive_datetime')
    list_filter = ('receive_datetime', )
    search_fields = ('receive_datetime', )
