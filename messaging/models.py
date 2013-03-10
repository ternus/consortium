from hashlib import md5
import subprocess
from django.db import models, IntegrityError
from django.conf import settings
from django.shortcuts import get_object_or_404
from consortium.consortium import send_mail
from hexgrid.models import Character
from succession.models import Line
from twilio.rest import TwilioRestClient

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

    @classmethod
    def mail_to(cls, char, subject, message, sender="System", urgent=False):
        msg = cls.objects.create(
            sender=Mailbox.objects.get_or_create(name=sender, type=0)[0],
            to=get_object_or_404(Mailbox, character=char, type=1),
            subject=subject,
            text=message
        )
        if char.routine_sms:
            Message.sms_to_char(char, "New Mail: %s" % subject)
        elif urgent and char.urgent_sms:
            Message.sms_to_char(char, "New Urgent Mail: %s" % subject)
        if char.contact_email:
            Message.mail_to_char(char)
        if char.contact_zephyr:
            Message.zephyr_to_char(char)
        return msg

    @classmethod
    def mail_line(cls, line, subject, message, sender="System"):
        if line == None: return None
        msg = cls.objects.create(
            sender=Mailbox.objects.get_or_create(name=sender, type=0)[0],
            to=get_object_or_404(Mailbox, line=line, type=2),
            subject=subject,
            text=message
        )
        return msg

    @classmethod
    def mail_to_char(cls, char):
        if not char.user.email: return None
        return send_mail("[Consortium] New in-game mail", "You have a new in-game mail.  Go to http://consortium.so/mail/ to check it.", "consortium-gms@cternus.net", [char.user.email], fail_silently=True)

    @classmethod
    def zephyr_to_char(cls, char):
        if not char.zephyr: return None
        if " " in char.zephyr: return None
        return subprocess.call("zwrite -d %s -m 'You have new Consortium mail. http://consortium.so/mail/'" % char.zephyr, shell=True)

    @classmethod
    def sms_to_char(cls, char, message):
        if not char.phone: return None
        client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
        return client.sms.messages.create(to=char.phone, from_=settings.TWILIO_PHONE_NUMBER, body="[Consortium] %s" % message)

MAILBOX_TYPES = (
    (0, 'System'),
    (1, 'Characters'),
    (2, 'Groups'),
    (3, 'Secret'),
    (4, 'Other')
)

class Mailbox(models.Model):
    name = models.CharField(max_length=settings.ML)
    code = models.CharField(max_length=settings.ML, blank=True)
    character = models.ForeignKey(Character, null=True, blank=True)
    type = models.IntegerField(default=1, choices=MAILBOX_TYPES)
    line = models.OneToOneField(Line, null=True, blank=True)
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