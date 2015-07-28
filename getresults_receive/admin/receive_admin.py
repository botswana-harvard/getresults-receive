from django.contrib import admin

from ..models import Receive


class ReceiveAdmin(admin.ModelAdmin):
    model = Receive
admin.site.register(Receive, ReceiveAdmin)