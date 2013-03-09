# Create your views here.
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from consortium.consortium import check_inspiration
from hexgrid.views import gtc
from messaging.models import Message
from security.models import EntryWindow, SecureLocation, SecurityWindow
from dateutil.parser import parse

@login_required()
def security(request, template='security/security.html'):
    char = gtc(request)
    if request.method == 'POST':
        if request.POST.get('type') == 'entry':
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
                new = EntryWindow.objects.create(location=location, start_time=time, creator=char, person=request.POST.get('person'))
                count = check_collisions_and_notify(new).count()
                messages.success(request, "Window created!")
                check_inspiration(request)
            except ValidationError, e:
                messages.error(request, e.messages[0])
        else:
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
                new = SecurityWindow.objects.create(location=location, start_time=time, creator=char)
                # count = check_collisions_and_notify(new).count()
                messages.success(request, "Window created!")
                check_inspiration(request)
            except ValidationError, e:
                messages.error(request, e.messages[0])

    entry_windows = EntryWindow.objects.filter(creator=char)
    security_windows = SecurityWindow.objects.filter(creator=char)
    owned_locations = SecureLocation.objects.filter(controller__lineorder__order=1, controller__lineorder__character=char)
    return render(request, template, {'entry_windows': entry_windows, 'security_windows': security_windows, 'owned_locations': owned_locations})

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

def check_collisions_and_notify(new_window):
    query_set = new_window.overlaps()
    if isinstance(new_window, EntryWindow):
        for s in query_set:
            Message.mail_to(s.creator, "Security Window Triggered",
                            "Security alert! Possible breach attempt at %s, time: %s" % (new_window.location, new_window.start_time), sender="Security")
    elif isinstance(new_window, SecurityWindow):
        for e in query_set:
            Message.mail_to(new_window.creator, "Security Window Triggered",
                            "Security alert! Possible breach attempt at %s, time: %s" % (new_window.location, e.start_time), sender="Security")
    return query_set