# coding=utf-8
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.urlresolvers import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from consortium.consortium import send_mail
from models import AppForm, ConsortiumApp


def app(request, app_id=None):
    game_time = datetime(2013,3,1,6)
    readonly = request.GET.get('readonly', False)
    if request.method == 'POST':
        try:
            instance = ConsortiumApp.objects.get(app_id=app_id)
        except ConsortiumApp.DoesNotExist:
            instance = None
        form = AppForm(request.POST, instance=instance)
        if form.is_valid():
            if request.POST['app_submit'] == 'Save and Continue Editing':
                app = form.save(commit=False)
                app.saved_on = datetime.now()
                app.save()
                if not instance:
                    send_mail("[Consortium] Your App Link",
                        render_to_string('app/app_saved_email.html', {'app': app}),
                        "consortium-gms@cternus.net",
                        [app.email], fail_silently=True, html=render_to_string('app/app_saved_email.html', {'app': app}),
                    )
                messages.success(request, 'Saved! You can continue editing, but make sure to save or submit when you\'re done.')
                return redirect(reverse('app', args=[app.app_id]))
            else:
                app = form.save(commit=False)
                app.apped_on = datetime.now()
                app.submitted = True
                app.save()
                form = AppForm(instance=app)
                send_mail("[Consortium] App from %s" % app.name,
                    render_to_string('app/app_email.html', {'form': form}),
                    "consortium-gms@cternus.net",
                    ['consortium-gms@mit.edu', app.email], html=render_to_string('app/app_email.html', {'form': form}),
                )
                return render(request, "app/postapp.html", {'app': app})
        else:
            messages.error(request, "Please correct the problems below.")
#            return redirect(reverse('app'))
    elif app_id:
        app = get_object_or_404(ConsortiumApp, app_id=app_id)
        form = AppForm(instance=app)
        readonly = request.GET.get('readonly', app.submitted)
    else:
        form = AppForm()
#    messages.success(request, 'test success')
#    messages.info(request, 'test info')
#    messages.error(request, 'test error')
#    messages.warning(request, 'test warning')

    return render(request, "app/app.html", {'form': form, 'app_id': app_id, 'game_time': game_time, 'readonly': readonly})

@login_required()
def dashboard(request):
    apps = ConsortiumApp.objects.all()
    due_time = naturaltime(datetime(2013,3,1,6))
    complete_apps = apps.filter(submitted=True)
    incomplete_apps = apps.filter(submitted=False)
    return render(request, "app/dashboard.html", {'apps': apps,
                                                  'complete_apps': complete_apps,
                                                  'incomplete_apps': incomplete_apps,
                                                  'due_time': due_time})

def remind(request, app_id):
    app = get_object_or_404(ConsortiumApp, app_id=app_id)
    due_time = naturaltime(datetime(2013,3,1,6))
    send_mail("[Consortium] App Reminder",
    render_to_string('app/app_reminder.html', {'app': app, 'due_time': due_time}),
    "consortium-gms@cternus.net",
    [app.email], fail_silently=True, html=render_to_string('app/app_reminder.html', {'app': app, 'due_time': due_time})
    )
    messages.success(request, "Reminded %s." % True)
    return redirect(reverse('dashboard'))

