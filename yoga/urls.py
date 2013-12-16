from django.conf.urls import patterns, include, url

from django.contrib import admin
from lessons import views
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^lessons/', include('lessons.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'lessons/index.html'}),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'lessons/logout.html'}),
)
