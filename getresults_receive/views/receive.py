from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def receive_batch(request):
    return HttpResponseRedirect(reverse('receive_batch'))


def receive_sample(request):
    return HttpResponseRedirect(reverse('receive_sample'))
