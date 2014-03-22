from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from tastypie.http import HttpUnauthorized, HttpForbidden
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from django.shortcuts import get_object_or_404
from lessons.models import Lesson, RegisteredStudent


class UserResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        #excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        fields = ['first_name', 'last_name', 'email']
        allowed_methods = ['get', 'post']
        include_resource_uri = False
        #authentication = BasicAuthentication()
        authorization = Authorization()
        
    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/login%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),
#             url(r'^(?P<resource_name>%s)/logout%s$' %
#                 (self._meta.resource_name, trailing_slash()),
#                 self.wrap_view('logout'), name='api_logout'),
        ]
        
    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return self.create_response(request, {
                    'success': True
                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                    }, HttpForbidden )
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
                }, HttpUnauthorized )

    def logout(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        if request.user and request.user.is_authenticated():
            logout(request)
            return self.create_response(request, { 'success': True })
        else:
            return self.create_response(request, { 'success': False }, HttpUnauthorized)


class LessonResource(ModelResource):
    #user = fields.ForeignKey(UserResource,'user')
    students = fields.ManyToManyField(UserResource, 'students', full=True)

    # TODO - need to figure out what to do with hydrate/dehydrate when patching!
    # Currently it modifies the users!!!
    
    class Meta:
        queryset = Lesson.objects.all()
        #authorization = DjangoAuthorization()
        allowed_methods = ['get', 'post', 'patch']
        #include_resource_uri = False
        excludes = ['id']
        resource_name = 'lesson'
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/signup%s$' %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('signup'), name="api_signup"),
             url(r'^(?P<resource_name>%s)/remove%s$' %
                 (self._meta.resource_name, trailing_slash()),
                 self.wrap_view('remove'), name='api_remove'),
        ]


    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        lesson_id = data.get('lesson', '')

        student = get_object_or_404(User, username=username)
        lesson = get_object_or_404(Lesson, id=lesson_id)
        rs = RegisteredStudent(lesson=lesson,student=student)
        rs.save()
        return self.create_response(request, { 'success': True })

    def remove(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        lesson_id = data.get('lesson', '')

        student = get_object_or_404(User, username=username)
        lesson = get_object_or_404(Lesson, id=lesson_id)
        rs = get_object_or_404(RegisteredStudent, lesson=lesson,student=student)
        rs.delete()
        return self.create_response(request, { 'success': True })





