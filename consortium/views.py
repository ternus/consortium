import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from gametex.models import GameTeXFieldValue
from hexgrid.models import Character
from hexgrid.views import gtc

@login_required()
def char_list(request, template="consortium/char_list.html"):
    context = {
        'characters': Character.objects.all()
    }
    return render(request, template, context)

@login_required()
def char_profile(request, char_id, template="consortium/char_profile.html"):
    char = gtc(request)
    p_char = get_object_or_404(Character, id=char_id)
    fields = GameTeXFieldValue.objects.filter(object=p_char.gto)
    context = {
        'request_char': char,
        'char': p_char,
        'fields': fields
    }

    return render(request, template, context)

@login_required()
def char_prefs(request, char_id):
    context = {}
    if request.method == 'POST':
        try:
            char = Character.objects.get(id=char_id)

            char.phone = request.POST.get('phone')
            u = char.user
            u.email = request.POST.get('email')

            char.zephyr = request.POST.get('zephyr')
            char.contact_email = request.POST.get('contact_email', False)
            char.contact_zephyr = request.POST.get('contact_zephyr', False)
            char.urgent_sms = request.POST.get('urgent_sms', False)
            char.routine_sms = request.POST.get('routine_sms', False)

            char.save()
            u.save()
            context['status'] = 'iconized icon-ok-circle'
            context['message'] = 'OK'

        except Exception, e:
            context['status'] = 'iconized icon-error'
            context['message'] = 'Server error: %s %s' % (e.message, type(e))

        return HttpResponse(json.dumps(context), mimetype="application/json")
