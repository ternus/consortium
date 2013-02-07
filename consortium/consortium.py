# coding=utf-8
"""
Miscellaneous stuff that didn't fit anywhere else.
"""
from hexgrid.models import HGCharacter, GameDay
from succession.models import LineOrder
from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading

def consortium_context(request):
    try:
        char = HGCharacter.objects.get(user=request.user)
    except HGCharacter.DoesNotExist:
        char = None
    except AttributeError:
        char = None
    except TypeError:
        char = None
    game_day = GameDay.get_day()
    has_lines = LineOrder.objects.filter(character=char).exists()
    return {'char': char,
            'game_day': game_day,
            'has_lines': has_lines}


class EmailThread(threading.Thread):
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.send(self.fail_silently)

def send_mail(subject, body, from_email, recipient_list, fail_silently=False, html=None, *args, **kwargs):
    EmailThread(subject, body, from_email, recipient_list, fail_silently, html).start()


class AppRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        if model._meta.app_label == 'app':
            return 'app_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'auth':
            return 'app_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'app' or\
           obj2._meta.app_label == 'app':
            return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'app_db':
            return model._meta.app_label == 'app'
        elif model._meta.app_label == 'app':
            return False
        return None
