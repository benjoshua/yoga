from django.conf.urls import patterns, include, url
from django.contrib import admin
from lessons import views
from django.core.urlresolvers import reverse_lazy


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^lessons/', include('lessons.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'lessons/index.html'}, name="login"),
    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('index')}, name="logout"),

)

