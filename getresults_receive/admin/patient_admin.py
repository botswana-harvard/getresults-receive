from django.contrib import admin

from ..models import Patient


class PatientAdmin(admin.ModelAdmin):
    model = Patient
admin.site.register(Patient, PatientAdmin)
