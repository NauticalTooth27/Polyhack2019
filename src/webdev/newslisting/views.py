#from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponseRedirect
#from django.urls import reverse
#from django.views import generic
from django.http import HttpResponse
from django.shortcuts import loader

from .models import Topic, Article, Quote

def index(request):
    latest_topics_list = Topic.objects.order_by('-pub_date')[:5]
    template = loader.get_template('newslisting/index.html')
    context = {
        'latest_topics_list': latest_topics_list,
    }
    return HttpResponse(template.render(context, request))

def topic(request, topic_id):
    return HttpResponse("You're looking at topic %s." % topic_id)

def info(request):
    return HttpResponse("You're looking at the info page.")
