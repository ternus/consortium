# coding=utf-8
from datetime import datetime
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from models import AppForm, ConsortiumApp

def app(request, app_id=None):
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            if request.POST['app_submit'] == 'Save App':
                app = form.save(commit=False)
                app.saved_on = datetime.now()
                app.save()
            else:
                app = form.save(commit=True)
                return render(request, "app/postapp.html", {'app': app})
    elif app_id:
        app = get_object_or_404(ConsortiumApp, app_id=app_id)
        form = AppForm(app)
    else:
        form = AppForm()
    return render(request, "app/app.html", {'form': form})