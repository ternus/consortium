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

@login_required()
def my_lines(request, template="lines/lines.html"):
    gtu = get_object_or_404(GameTeXUser, user=request.user)
    lines = Line.objects.filter(members=gtu)
    context = {
        "lines": lines,
    }
    return render(request, template, {"lines": lines})

@login_required()
def show_line(request, line_id, template="lines/show_line.html"):
    gtu = get_object_or_404(GameTeXUser, user=request.user)
    line = get_object_or_404(Line, id=line_id)
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
    membership = get_object_or_404(LineOrder, character=gtu)
    context = {
        "line": line,
        "line_members": line.members.all().order_by('lineorder'),
        "membership": membership,
    }
    return render(request, template, context)
