from django.urls import path

from . import views

app_name = 'newslisting'
urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.IndexView.as_view(), name='index'),
    #path('/info', views.IndexView.as_view(), name='info'),
    #path('<int:pk>/', views.DetailView.as_view(), name='topic'),
]
