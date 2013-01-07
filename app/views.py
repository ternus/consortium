# coding=utf-8
from django.contrib import messages

from django.shortcuts import render, redirect
from models import AppForm

def app(request):
    if request.method == 'POST':
        form = AppForm(request.POST)
        print form
        print form.is_valid()
        if form.is_valid():
            messages.success(request, 'Thank you for applying!')
            form.save(commit=True)
            return redirect('/')
    else:
        form = AppForm()
    return render(request, "app/app.html", {'form': form})