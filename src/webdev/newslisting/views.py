from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
#from django.http import HttpResponse
#from django.shortcuts import loader

from .models import Topic, Article

class IndexView(generic.ListView):
    template_name = 'newslisting/index.html'
    context_object_name = 'latest_topics_list'

    def get_queryset(self):
        return Topic.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Topic
    template_name = 'newslisting/topic.html'

def info(request):
    return HttpResponse("You're looking at the info page.")
