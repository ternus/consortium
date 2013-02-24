from coverage.backward import md5
from django.db import models
from django.conf import settings
from hexgrid.models import Character
from succession.models import Line

class Message(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=False)
    sender = models.ForeignKey('Mailbox', related_name='mail_sender')
    subject = models.CharField(max_length=settings.ML)
    anon = models.BooleanField(default=False)
    to = models.ForeignKey('Mailbox', related_name='mail_recipient')
    text = models.TextField()

    def __unicode__(self):
        return "From: %s To: %s Time: %s Subject: %s" % (self.sender, self.to, self.time, self.subject)

MAILBOX_TYPES = (
    (0, 'Special'),
    (1, 'Characters'),
    (2, 'Groups'),
    (3, 'Secret'),
    (4, 'Other')
)

class Mailbox(models.Model):
    name = models.CharField(max_length=settings.ML)
    code = models.CharField(max_length=settings.ML, blank=True)
    character = models.ForeignKey(Character, null=True)
    type = models.IntegerField(default=1, choices=MAILBOX_TYPES)
    line = models.OneToOneField(Line, null=True)
    public = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def display_name(self):
        return self.name if self.public else "Anonymous"

    def mail(self):
        return Message.objects.filter(to=self).order_by('-time')

    def sent_mail(self):
        return Message.objects.filter(sender=self).order_by('-time')

    def unread_mail(self):
        return Message.objects.filter(to=self, viewed=False)

    def save(self, **kwargs):
        if not self.code:
            self.code = md5(self.name).hexdigest()[:4].upper()
        return super(Mailbox, self).save(**kwargs)