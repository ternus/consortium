# coding=utf-8
"""
Miscellaneous stuff that didn't fit anywhere else.
"""
from random import random, choice
from django.contrib import messages
from django.db.models import Q
from hexgrid.models import Character, GameDay
from succession.models import LineOrder, Line
from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading


def consortium_context(request):
    """
    Get important Consortium variables into the request
    :param request: request object
    :return: none
    """
    from messaging.models import Mailbox

    mboxes = []
    try:
        char = Character.objects.get(user=request.user)
        mboxes = Mailbox.objects.filter(Q(character=char) | Q(line__lineorder__order=1, line__lineorder__character=char))
    except Character.DoesNotExist:
        char = None
    except AttributeError:
        char = None
    except TypeError:
        char = None
    game_day = GameDay.get_day()
    has_lines = LineOrder.objects.filter(character=char).exists()
    has_wargame = Line.objects.filter(lineorder__character=char).exclude(faction=None).exists()
    if request.user.is_superuser: mboxes = Mailbox.objects.filter(name__contains='GM')
    unread = sum(map(lambda x: len(x.unread_mail()), mboxes))
    return {'char': char,
            'game_day': game_day,
            'has_lines': has_lines,
            'has_wargame': has_wargame,
            'gm': request.user.is_superuser,
            'unread': unread,
            'mboxes': mboxes}


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

def post_import():
    for c in Character.objects.all():
        m = Mailbox.objects.create(type=1, character=c, name=c.gto.name)

inspir_msgs = ['Congratulations', 'Ding', 'Surprise', 'Huzzah', 'It\'s your lucky day']

def check_inspiration(request):
    if random() <= .25:
        messages.info(request, "%s! You gain 1 inspiration." % choice(inspir_msgs))