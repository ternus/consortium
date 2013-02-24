# Create your views here.
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import render
from hexgrid.views import gtc
from security.models import EntryWindow, SecureLocation, SecurityWindow
from dateutil.parser import parse

@login_required()
def security_window(request, template='security/security_window.html'):
    char = gtc(request)
    if request.method == 'POST':
        try:
            time = parse(request.POST.get('time'))
        except ValueError:
            raise ValidationError("Invalid time; window not created.")
        if time < datetime.now():
            raise ValidationError("Start time must be in the future.")
        try:
            location = SecureLocation.objects.get(room=request.POST.get('room').strip())
        except SecureLocation.DoesNotExist:
            raise ValidationError("No secure location in room %s." % request.POST.get('room').strip())
        SecurityWindow.objects.create(location=location, start_time=time, creator=char)
        messages.success(request, "Window created!")
    current_windows = SecurityWindow.objects.filter(creator=char)
    owned_locations = SecureLocation.objects.filter(controller__lineorder__order=1, controller__lineorder__character=char)
    return render(request, template, {'current_windows': current_windows, 'owned_locations': owned_locations})

@login_required()
def entry_window(request, template='security/entry_window.html'):
    char = gtc(request)
    if request.method == 'POST':
        try:
            try:
                time = parse(request.POST.get('time'))
            except ValueError:
                raise ValidationError("Invalid time; window not created.")
            if time < datetime.now():
                raise ValidationError("Start time must be in the future.")
            try:
                location = SecureLocation.objects.get(room=request.POST.get('room').strip())
            except SecureLocation.DoesNotExist:
                raise ValidationError("No secure location in room %s." % request.POST.get('room').strip())
            EntryWindow.objects.create(location=location, start_time=time, creator=char, person=request.POST.get('person'))
            messages.success(request, "Window created!")
        except ValidationError, e:
            messages.error(request, e.messages[0])
    current_windows = EntryWindow.objects.filter(creator=char)
    return render(request, template, {'current_windows': current_windows})

@login_required()
def gm_security(request, template="security/gm.html"):
    if not request.user.is_superuser:
        raise Http404
    context = {
        'secure_locations': SecureLocation.objects.all(),
        'entry_windows':  EntryWindow.objects.all(),
        'security_windows':  SecurityWindow.objects.all()
    }
    return render(request, template, context)

def check_collisions(new_window):
    if isinstance(new_window, EntryWindow):
        pass