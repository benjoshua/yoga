from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from lessons.forms import UserCreateForm
from django.views import generic
import datetime
from lessons.models import Lesson, RegisteredStudent
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from lessons.serializers import LessonSerializer, LessonDetailSerializer, UserSerializer



class IndexView(generic.ListView):
    model = Lesson
    template_name = 'lessons/index.html'
    context_object_name = 'lessons'
    def get_queryset(self):
        return Lesson.objects.filter(date__gte=datetime.date.today()).order_by('date')[:4]


def register(request):
    if request.method == 'POST':
        registration_form = UserCreateForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/lessons/")
    else:
        registration_form = UserCreateForm()
    return render(request, "lessons/register.html", {
        'registration_form': registration_form
    })

@login_required
def signup(request, lesson_id, student_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = get_object_or_404(User, id=student_id)
    rs = RegisteredStudent(lesson=lesson,student=student)
    rs.save()
    return redirect("/lessons/")

@login_required
def remove(request, lesson_id, student_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = get_object_or_404(User, id=student_id)
    rs = get_object_or_404(RegisteredStudent, lesson=lesson,student=student)
    rs.delete()
    return redirect("/lessons/")

class LessonList(generics.ListAPIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    model = Lesson
    serializer_class = LessonSerializer

@api_view(['GET'])
def lesson_detail(request, pk, format=None):
    try:
        lesson = Lesson.objects.get(id=pk)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LessonDetailSerializer(lesson)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def signup_api(request,format=None):

    username = request.DATA.get('username', '')
    lesson_id = request.DATA.get('lesson', '')

    if request.user != username:
        content = {'Not authorized to sign up': 'For a different user'}
        return Response(content, status=status.HTTP_401_UNAUTHORIZED)

    student = get_object_or_404(User, username=username)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    rs = RegisteredStudent(lesson=lesson,student=student)
    rs.save()

    #TODO - handle case when class if full and notify students

    return Response({ 'success': True })

@api_view(['POST'])
def login_api(request,format=None):

        username = request.DATA.get('username', '')
        password = request.DATA.get('password', '')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                content = {'success': True}
                return Response(content)
            else:
                content = {
                'success': False,
                'reason': 'incorrect',
                }
                return Response(content, status=status.HTTP_403_FORBIDDEN)
        else:
            content = {
                'success': True,
                'reason': 'incorrect',
            }
            return Response(content, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def logout_api(request,format=None):

    if request.user and request.user.is_authenticated():
        logout(request)
        return Response({ 'success': True })
    else:
        return Response({ 'success': False }, status=status.HTTP_403_FORBIDDEN)