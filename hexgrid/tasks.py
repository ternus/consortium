from datetime import datetime
from consortium.consortium import send_mail
from hexgrid.models import GameDay
from celery.schedules import crontab
from celery.task import periodic_task

__author__ = 'cternus'

@periodic_task(run_every=crontab(minute='0', hour='6'))
def market_tick():
    msg = GameDay.tick()
    send_mail("[Consortium] Tick!", "Tick successful at %s" % datetime.now(), 'consortium-gms@cternus.net',
              ['ternus@mit.edu'], fail_silently=True)