from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth import authenticate, login
from lessons.models import Lesson
from lessons.forms import UserCreateForm
import datetime

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
        'registration_form': registration_form,
    })

def signup(request, lesson_id, student_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = get_object_or_404(User, id=student_id)
    lesson.students.add(student)
    return redirect("/lessons/")

def remove(request, lesson_id, student_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    student = get_object_or_404(User, id=student_id)
    lesson.students.remove(student)
    return redirect("/lessons/")