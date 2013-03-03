from datetime import timedelta
from django.db import models
from django.conf import settings
from django.db.models import Q
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

    def overlaps(self):
        return SecurityWindow.objects.filter(location=self.location).filter(
            Q(Q(start_time__lt=self.end_time) & Q(end_time__gt=self.end_time)) | Q(
                Q(start_time__lt=self.start_time) & Q(end_time__lt=self.end_time)) | Q(
                Q(start_time__lt=self.start_time) & Q(end_time__gt=self.end_time)))


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

    def overlaps(self):
        return EntryWindow.objects.filter(location=self.location).filter(
            Q(Q(start_time__lte=self.start_time) & Q(end_time__gt=self.start_time)) | Q(
                Q(start_time__gte=self.start_time) & Q(end_time__lte=self.end_time)) | Q(
                Q(start_time__lte=self.start_time) & Q(end_time__gte=self.start_time)))
