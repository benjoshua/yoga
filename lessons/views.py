from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from lessons.models import Lesson

#@login_required
class IndexView(generic.ListView):
    model = Lesson
    template_name = 'lessons/details.html'
    context_object_name = 'lessons'
    def get_queryset(self):
        return Lesson.objects.all()