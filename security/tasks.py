from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task
from django.utils.timezone import now
from consortium.consortium import send_mail
from security.models import EntryWindow

__author__ = 'cternus'

@periodic_task(run_every=crontab(minute='*', hour='*'))
def check_security_windows():
    windows = EntryWindow.objects.filter(start_time__lte=now(), start_time__gt=now() - timedelta(hours=1))
    for w in windows:
        if w.check_and_notify():
            send_mail("[Consortium] Security window alert!", "Security window triggered: %s" % w, 'consortium-gms@cternus.net',
                  ['ternus@mit.edu'], fail_silently=True)
