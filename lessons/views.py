from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # Login page or lessons if connected
    return render(request, 'lessons/index.html')