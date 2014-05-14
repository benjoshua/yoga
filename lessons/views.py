
from django.contrib.auth import authenticate, login
from lessons.forms import UserCreateForm
from django.views import generic
import datetime
from lessons.models import Lesson
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect



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

def attend(request):
    try:
        value = request.POST['remove']
        action = 'remove'
    except (KeyError):
        try:
            value = request.POST['attend']
            action = 'attend'
        except (KeyError):
            return redirect('index')
    
    try:
        selected_lesson = Lesson.objects.get(pk=value)
    except (Lesson.DoesNotExist):
        return redirect('index')
    
    if action == 'remove':
        selected_lesson.students.remove(request.user)
        messages.info(request, "You were removed from lesson :-) Hope to See you soon!")
    elif action == 'attend':
        selected_lesson.students.add(request.user)
        messages.success(request, "You were successfully signed up :-) See you there!")
    selected_lesson.save()
    return redirect('index')

    selected_lesson.save()
    return redirect('index')

def lessonsPanel(request):
        return render(request, "lessons/panel.html", {

    })

