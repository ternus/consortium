# coding=utf-8
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
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
    gtu = get_object_or_404(GameTeXUser, user=request.user)
    lines = Line.objects.filter(members=gtu)
    return render(request, template, {"lines": lines})

@login_required()
def show_line(request, line_id, template="lines/show_line.html"):
    gtu = None
    if not request.user.is_superuser:
        gtu = get_object_or_404(GameTeXUser, user=request.user)
    line = get_object_or_404(Line, id=line_id)
    line_controls = []
    try:
        line_controls += ['The mailbox %s' % line.mailbox.name]
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
        from_membership = get_object_or_404(LineOrder, character__user=promoted_user)
        print from_membership.character, from_membership.order
        to_membership = get_object_or_404(LineOrder, order=from_membership.order - 1)
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

        return redirect('show_line', line_id)
    if not request.user.is_superuser:
        membership = get_object_or_404(LineOrder, character=gtu)
    else:
        membership = None
    context = {
        "line": line,
        "line_controls": line_controls,
        "line_members": line.members.all().order_by('lineorder'),
        "membership": membership,
    }
    return render(request, template, context)
