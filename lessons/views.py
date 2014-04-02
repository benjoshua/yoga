from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from lessons.forms import UserCreateForm
from django.views import generic
import datetime
from lessons.models import Lesson, RegisteredStudent
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    model = Lesson
    serializer_class = LessonSerializer

class LessonDetail(generics.RetrieveAPIView):
    model = Lesson
    serializer_class = LessonDetailSerializer
    lookup_field = 'id'

class UserDetail(generics.RetrieveAPIView):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'username'

@api_view(['GET'])
def lesson_list(request, format=None):
    lessons = Lesson.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def lesson_detail(request, pk, format=None):
    try:
        lesson = Lesson.objects.get(id=pk)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LessonDetailSerializer(lesson)
    return Response(serializer.data)

@api_view(['POST'])
def signup_api(request,format=None):
    username = request.DATA.get('username', '')
    lesson_id = request.DATA.get('lesson', '')

    student = get_object_or_404(User, username=username)
    lesson = get_object_or_404(Lesson, id=lesson_id)
    rs = RegisteredStudent(lesson=lesson,student=student)
    rs.save()

    return Response({ 'success': True })