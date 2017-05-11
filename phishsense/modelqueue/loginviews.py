from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse


def signin(request):
    context = {}
    return render(request, 'modelqueue/signin.html', context)

