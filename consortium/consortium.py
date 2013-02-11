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
    """
    Get important Consortium variables into the request
    :param request: request object
    :return: none
    """

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
            'has_lines': has_lines,
            'gm': request.user.is_superuser}


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


