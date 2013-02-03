# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required()
def overview(request, template):

    return render(request, template, {})