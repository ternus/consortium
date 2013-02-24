from datetime import timedelta
from django.db import models
from django.conf import settings
from hexgrid.models import Character
from succession.models import Line


class SecureLocation(models.Model):
    name = models.CharField(max_length=settings.ML, unique=True)
    room = models.CharField(max_length=settings.ML, unique=True)
    controller = models.ForeignKey(Line, null=True)
    entry_cost = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.room)


class EntryWindow(models.Model):
    creator = models.ForeignKey(Character)
    location = models.ForeignKey(SecureLocation)
    person = models.CharField(max_length=settings.ML, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(editable=False)

    def __unicode__(self):
        return "%s entering %s at %s" % (self.creator, self.location, self.start_time)

    def save(self, **kwargs):
        self.end_time = self.start_time + timedelta(minutes=settings.ENTRY_WINDOW_MINUTES)
        return super(EntryWindow, self).save(**kwargs)


class SecurityWindow(models.Model):
    creator = models.ForeignKey(Character)
    location = models.ForeignKey(SecureLocation)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(editable=False)

    def save(self, **kwargs):
        self.end_time = self.start_time + timedelta(minutes=settings.SECURITY_WINDOW_MINUTES)
        return super(SecurityWindow, self).save(**kwargs)

    def __unicode__(self):
        return "%s securing %s at %s" % (self.creator, self.location, self.start_time)
