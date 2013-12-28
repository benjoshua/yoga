from django.conf.urls import patterns, url, include
from lessons.api import LessonResource, UserResource
from tastypie.api import Api
from lessons import views


v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(LessonResource())

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/', views.register, name='register'),
    (r'^api/', include(v1_api.urls)),
)