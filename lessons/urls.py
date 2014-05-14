from django.conf.urls import patterns, url

from lessons import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^attend/', views.attend, name='attend'),
    url(r'^panel/', views.lessonsPanel, name='lessonsPanel'),

)