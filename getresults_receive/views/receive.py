from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse


def receive_batch(request):
    return HttpResponseRedirect(reverse('receive_batch'))


def receive_sample(request):
    return HttpResponseRedirect(reverse('receive_sample'))
