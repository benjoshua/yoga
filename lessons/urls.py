from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from lessons.api import LessonResource, UserResource
from tastypie.api import Api
from lessons import views
from rest_framework.urlpatterns import format_suffix_patterns



v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(LessonResource())

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^index/', TemplateView.as_view(template_name='lessons/lessons.html'), name="home"),
    url(r'^register/', views.register, name='register'),
    url(r'^signup/(?P<lesson_id>\d+)/(?P<student_id>\d+)/$', views.signup, name='signup'),
    url(r'^remove/(?P<lesson_id>\d+)/(?P<student_id>\d+)/$', views.remove, name='remove'),
    (r'^api/', include(v1_api.urls)),
    #url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest_api/$', views.LessonList.as_view()),
    url(r'^rest_api/RegisteredStudents/$', views.RegisteredStudentsList.as_view()),
    url(r'^rest_api/(?P<pk>\d+)$', 'lessons.views.lesson_detail', name='lesson_detail'),
    url(r'^rest_api/(?P<pk>\d+)/attended/$', 'lessons.views.attended_api'),
    url(r'^rest_api/signup/$', 'lessons.views.signup_api'),
    url(r'^rest_api/remove/$', 'lessons.views.remove_api'),
    url(r'^rest_api/login/$', 'lessons.views.login_api'),
    url(r'^rest_api/logout/$', 'lessons.views.logout_api'),

)

urlpatterns = format_suffix_patterns(urlpatterns)