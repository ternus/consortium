from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task
from django.utils.timezone import now
from security.models import EntryWindow

__author__ = 'cternus'

@periodic_task(run_every=crontab(minute='*', hour='*'))
def check_security_windows():
    windows = EntryWindow.objects.filter(start_time__lte=now(), start_time__gt=now() - timedelta(hours=1))
    for w in windows:
        w.check_and_notify()