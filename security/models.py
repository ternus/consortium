from datetime import timedelta, datetime
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils.timezone import localtime, make_aware
from hexgrid.models import Character
from messaging.models import Message
from succession.models import Line

DST_START = make_aware(datetime(2013, 3, 10, 1, 59))
DST_END = make_aware(datetime(2013, 3, 10, 3, 1))

class SecureLocation(models.Model):
    name = models.CharField(max_length=settings.ML)
    room = models.CharField(max_length=settings.ML, unique=True)
    controller = models.ForeignKey(Line, null=True, blank=True)
    entry_cost = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.room)


class EntryWindow(models.Model):
    creator = models.ForeignKey(Character)
    location = models.ForeignKey(SecureLocation)
    person = models.CharField(max_length=settings.ML, unique=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(editable=False)
    notified = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s entering %s at %s" % (self.creator, self.location, self.start_time)

    def save(self, **kwargs):

        if self.start_time >= DST_START and self.start_time <= DST_END:
            self.start_time = DST_START

        self.end_time = self.start_time + timedelta(minutes=settings.ENTRY_WINDOW_MINUTES)

        if self.end_time >= DST_START and self.end_time <= DST_END:
            self.end_time = DST_END

        return super(EntryWindow, self).save(**kwargs)

    def overlaps(self):
        return SecurityWindow.objects.filter(location=self.location).filter(
            Q(Q(start_time__lt=self.end_time) & Q(end_time__gt=self.end_time)) | Q(
                Q(start_time__lt=self.start_time) & Q(end_time__lt=self.end_time)) | Q(
                Q(start_time__lt=self.start_time) & Q(end_time__gt=self.end_time)))

    def check_and_notify(self):
        if self.notified == True: return
        for s in self.overlaps():
            if s.creator.alive:
                Message.mail_to(s.creator, "Security Alarm: %s" % self.location,
                "Security alert! Entry window detected; possible breach attempt in progress at %s, start time: %s" % (
                self.location, localtime(self.start_time)), sender="Security", urgent=True)
        self.notified = True
        self.save()

class SecurityWindow(models.Model):
    creator = models.ForeignKey(Character)
    location = models.ForeignKey(SecureLocation)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(editable=False)

    def save(self, **kwargs):

        if self.start_time >= DST_START and self.start_time <= DST_END:
            self.start_time = DST_START

        self.end_time = self.start_time + timedelta(minutes=settings.SECURITY_WINDOW_MINUTES+1)

        if self.end_time >= DST_START and self.end_time <= DST_END:
            self.end_time = DST_END

        return super(SecurityWindow, self).save(**kwargs)

    def __unicode__(self):
        return "%s securing %s at %s" % (self.creator, self.location, self.start_time)

    def overlaps(self):
        return EntryWindow.objects.filter(location=self.location).filter(
            Q(Q(start_time__lte=self.start_time) & Q(end_time__gt=self.start_time)) | Q(
                Q(start_time__gte=self.start_time) & Q(end_time__lte=self.end_time)) | Q(
                Q(start_time__lte=self.start_time) & Q(end_time__gte=self.start_time)))
