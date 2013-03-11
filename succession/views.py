# coding=utf-8
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Max
from django.http import Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from hexgrid.models import Character
from messaging.models import Message, Mailbox
from models import Line, LineOrder
from gametex.models import GameTeXUser
from security.models import SecureLocation
from territory.models import Faction


@login_required()
def gm_lines(request, template="lines/lines.html"):
    lines = Line.objects.all()
    return render(request, template, {"lines": lines})

@login_required()
def my_lines(request, template="lines/lines.html"):
    if request.user.is_superuser: return redirect('gm_lines')
    gtu = get_object_or_404(GameTeXUser, user=request.user)
    lines = Line.objects.filter(members=gtu)
    return render(request, template, {"lines": lines})

@login_required()
def kill_character(request, template="lines/kill_character.html"):
    if not request.user.is_superuser: raise Http404
    if request.method == 'POST':
        char_id = request.POST.get('char', None)
        char = get_object_or_404(Character, id=char_id)
        really_dead = request.POST.get('really-dead', False)
        print really_dead
        if really_dead:
            char.alive = False
            char.save()
        for line in Line.objects.filter(members=char):
            lo = LineOrder.objects.get(line=line, character=char)
            los = LineOrder.objects.filter(line=line, order__gt=lo.order).order_by('order')
            orig_order = lo.order
            lo.order = 1000 + lo.id
            lo.save()
            for lox in los:
                lox.order -= 1
                lox.save()
            if really_dead:
                lo.delete()
                Message.mail_to(char, "You have been declared dead. Thanks for playing!", "You have been officially declared dead. Thanks for playing our game.", urgent=True)
            else:
                lo.order = LineOrder.objects.exclude(id=lo.id).filter(line=line, order__lt=lo.order).aggregate(Max('order'))['order__max'] + 1
                lo.save()
                Message.mail_to(char, "You have been declared missing.", "You have been officially declared missing, and demoted to the bottom of any groups you are in.", urgent=True)
            for c in line.members.exclude(id=char.id):
                message = "Notice to all members of %s:\n %s has been declared %s. \n" % (line.name, char.gto.name, "dead" if really_dead else "missing")
                message += "The cause: %s.\n" % request.POST.get('cause', 'Unknown')
                if orig_order == 1:
                    message += "%s is the new controller of %s." % (line.current_leader().character.gto.name, line.name)
                print c
                print Mailbox.objects.get(character=c, type=1)
                Message.mail_to(c, "%s Alert: %s" % ("Death" if really_dead else "Missing", char.gto.name),
                                message, sender="Mogadishu Office of Civil Security", urgent=True)
        messages.success(request, "%s was declared %s.  Mail sent." % (char.name, "dead" if really_dead else "missing"))

    return render(request, template, {'chars': Character.objects.filter(alive=True)})


@login_required()
def show_line(request, line_id, template="lines/show_line.html"):
    gtu = None
    if not request.user.is_superuser:
        gtu = get_object_or_404(Character, user=request.user)
        name = gtu.name
    else:
        name = "The GMs"
    line = get_object_or_404(Line, id=line_id)
    line_controls = []
    try:
        line_controls += ['The mailbox %s (code %s)' % (line.mailbox.name, line.mailbox.code)]
    except:
        pass
    try:
        line_controls += ['The territory control faction %s' % Faction.objects.get(controller=line).name]
    except Faction.DoesNotExist:
        pass
    for s in SecureLocation.objects.filter(controller=line):
        line_controls += ['The secure location %s' % s]
    promote = request.GET.get('promote', None)
    if promote:
        promoted_user = get_object_or_404(User, id=int(promote))
        from_membership = get_object_or_404(LineOrder, line=line, character__user=promoted_user)
        print from_membership.character, from_membership.order
        to_membership = get_object_or_404(LineOrder, line=line, order=from_membership.order - 1)
        print to_membership.character, to_membership.order
        # get around db column uniqueness enforcement
        neworder = to_membership.order
        from_membership.order = 999
        from_membership.save()
        to_membership.order += 1
        to_membership.save()
        from_membership.order = neworder
        from_membership.save()
        while not LineOrder.objects.filter(line=line, order=1).exists():
            for o in LineOrder.objects.filter(line=line).order_by('-order'):
                o.order -= 1
                o.save()
        Message.mail_to(from_membership.character, "Promotion Alert",
                        "%s promoted you in the %s line! Your new rank is %s. %s" % (name, line.name, from_membership.order, "You are now in charge." if from_membership.order == 1 else ""),
                        sender="Group Command")
        Message.mail_to(to_membership.character, "Demotion Alert",
                        "%s demoted you in the %s line. Your new rank is %s." % (name, line.name, to_membership.order),
                        sender="Group Command")
        return redirect('show_line', line_id)
    if not request.user.is_superuser:
        membership = get_object_or_404(LineOrder, character=gtu, line=line)
    else:
        membership = None
    context = {
        "line": line,
        "is_leader": line.current_leader().character == gtu,
        "line_controls": line_controls,
        "line_members": line.members.all().order_by('lineorder'),
        "membership": membership,
    }
    return render(request, template, context)
