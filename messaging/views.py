# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render
from hexgrid.views import gtc
from messaging.models import Message, Mailbox

@login_required()
def mail_home(request, template="messaging/mail_home.html"):
    char = gtc(request)
    context = {
        'special_mailboxes': Mailbox.objects.filter(public=True, type=0).order_by('name'),
        'char_mailboxes': Mailbox.objects.filter(public=True, type=1).order_by('name'),
        'group_mailboxes': Mailbox.objects.filter(public=True, type=2).order_by('name'),
        'mailboxes': Mailbox.objects.filter(Q(character=char) | Q(line__lineorder__order=1, line__lineorder__character=char))
    }
    if request.method == 'POST':
        try:
            context['mail_text'] = request.POST.get('text')
            new_mail = Message()
            new_mail.sender = Mailbox.objects.get(code=request.POST.get('from_code'))
            try:
                new_mail.to = Mailbox.objects.get(code=request.POST.get('to_code'))
            except Mailbox.DoesNotExist:
                try:
                    new_mail.to = Mailbox.objects.get(name=request.POST.get('to_name'))
                except Mailbox.DoesNotExist:
                    raise ValidationError("That mailbox doesn't exist.")
            new_mail.text = request.POST.get('text')
            new_mail.subject = request.POST.get('subject')
            print request.POST.get('anon') == 'on'
            new_mail.anon = request.POST.get('anon') == 'on'
            new_mail.save()
            print new_mail.anon
            messages.success(request, "Sent mail to %s" % new_mail.to.name)
            context['mail_text'] = ''
        except ValidationError, e:
            messages.error(request, e.messages[0])
    return render(request, template, context)


@login_required()
def gm_mail_home(request, template="messaging/mail_home.html"):
    if not request.user.is_superuser: raise Http404
    context = {
        'special_mailboxes': Mailbox.objects.filter(public=True, type=0).order_by('name'),
        'char_mailboxes': Mailbox.objects.filter(public=True, type=1).order_by('name'),
        'group_mailboxes': Mailbox.objects.filter(public=True, type=2).order_by('name'),
        'mailboxes': Mailbox.objects.all()
    }
    if request.method == 'POST':
        try:
            context['mail_text'] = request.POST.get('text')
            new_mail = Message()
            new_mail.sender = Mailbox.objects.get(code=request.POST.get('from_code'))
            try:
                new_mail.to = Mailbox.objects.get(code=request.POST.get('to_code'))
            except Mailbox.DoesNotExist:
                try:
                    new_mail.to = Mailbox.objects.get(name=request.POST.get('to_name'))
                except Mailbox.DoesNotExist:
                    raise ValidationError("That mailbox doesn't exist.")
            new_mail.text = request.POST.get('text')
            new_mail.subject = request.POST.get('subject')
            print request.POST.get('anon') == 'on'
            new_mail.anon = request.POST.get('anon') == 'on'
            new_mail.save()
            print new_mail.anon
            messages.success(request, "Sent mail to %s" % new_mail.to.name)
            context['mail_text'] = ''
        except ValidationError, e:
            messages.error(request, e.messages[0])
    return render(request, template, context)

def set_read(request):
    id = request.GET.get('id')
    m = Message.objects.get(id=id)
    if not (request.user.is_superuser and not 'GM' in m.to.name):
        m.viewed = True
    m.save()
    return HttpResponse('ok')
