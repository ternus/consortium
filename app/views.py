# coding=utf-8
from datetime import datetime
from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from models import AppForm, ConsortiumApp


def app(request, app_id=None):
    game_time = datetime(2013,3,1,6)
    if request.method == 'POST':
        try:
            instance = ConsortiumApp.objects.get(app_id=app_id)
        except ConsortiumApp.DoesNotExist:
            instance = None
        form = AppForm(request.POST, instance=instance)
        if form.is_valid():
            if request.POST['app_submit'] == 'Save App':
                app = form.save(commit=False)
                app.saved_on = datetime.now()
                app.save()
                msg = EmailMessage("[Consortium] Your App Link",
                    render_to_string('app/app_saved_email.html', {'app': app}),
                    "consortium-gms@cternus.net",
                    [app.email])
                msg.content_subtype = 'html'
                msg.send()

                return redirect(reverse('app', args=[app.app_id]))
            else:
                app = form.save(commit=False)
                app.apped_on = datetime.now()
                app.submitted = True
                app.save()
                form = AppForm(instance=app)
                msg = EmailMessage("[Consortium] App from %s" % app.name,
                    render_to_string('app/app_email.html', {'form': form}),
                    "consortium-gms@cternus.net",
                    ['consortium-gms@mit.edu'])
                msg.content_subtype = 'html'
                msg.send()
                return render(request, "app/postapp.html", {'app': app})
    elif app_id:
        app = get_object_or_404(ConsortiumApp, app_id=app_id)
        form = AppForm(instance=app)
    else:
        form = AppForm()
    return render(request, "app/app.html", {'form': form, 'app_id': app_id, 'game_time': game_time})