from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse


def receive_sample(request):
    patient = request.POST.get('patient_id')
    collect_datetime = request.POST.get('collect_datetime')
    print (patient)
    template = 'receive.html'
    return HttpResponseRedirect(reverse('receive'))
