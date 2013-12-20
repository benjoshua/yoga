from django.shortcuts import render

# Create your views here.

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

class IndexView(generic.ListView):
    model = Lesson
    template_name = 'lessons/index.html'
    context_object_name = 'lessons'
    def get_queryset(self):
        return Lesson.objects.order_by('date')[:4]


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/lessons/")
    else:
        form = UserCreationForm()
    return render(request, "lessons/register.html", {
        'form': form,
    })