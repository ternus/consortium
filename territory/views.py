# Create your views here.
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from hexgrid.views import gtc
from succession.models import Line
from territory.models import Unit, Faction, Territory, Action, GameBoard, validation_str, SPEC, SUPP, MOVE
from territory.somalia import somaliax as somalia_pts


@login_required()
def overview(request, template="territory/territory.html"):
    somalia = ",".join(["[%s,%s]" % (x[0], x[1]) for x in Territory.convert_points(somalia_pts)])
    user = gtc(request)
    faction_code = Line.by_char(user).exclude(faction_id='')[0].faction_id

    faction = get_object_or_404(Faction, code=faction_code)

    actions = Action.objects.filter(faction__code=faction_code, turn=GameBoard.get_turn())
    orders = {}
    for a in actions:
        orders[a.territory.code] = {
            'faction': a.faction.code,
            'turn': a.turn,
            'territory': a.territory.code,
            'type': a.type,
            'target': a.target.code,
            'special': a.special,
            'support_type': a.support_type,
            'support_to': a.support_to.code if a.support_to else None,
            'validation_level': validation_str(a.validation_level)
        }

    #    units = Unit.live_units().filter(faction=faction)
    territories = Territory.objects.all()
    context = {
        'faction': faction,
        'orders': json.dumps(orders),
        'somalia': somalia,
        'territories': territories,
    }
    return render(request, template, context)


@login_required()
def gm_overview(request, template="territory/territory.html"):
    if not request.user.is_superuser: raise Http404
    somalia = ",".join(["[%s,%s]" % (x[0], x[1]) for x in Territory.convert_points(somalia_pts)])

    actions = Action.objects.filter(turn=GameBoard.get_turn())
    orders = {}
    for a in actions:
        orders[a.territory.code] = {
            'str': str(a),
            'faction': a.faction.code,
            'turn': a.turn,
            'territory': a.territory.code,
            'type': a.type,
            'target': a.target.code,
            'special': a.special,
            'support_type': a.support_type,
            'support_to': a.support_to.code if a.support_to else None,
            'validation_level': validation_str(a.validation_level)
        }
    #    faction = get_object_or_404(Faction, code=faction_code)
    #    units = Unit.live_units().filter(faction=faction)
    territories = Territory.objects.all() #TODO can_see?
    context = {
        'orders': json.dumps(orders),
        'somalia': somalia,
        'territories': territories,
    }
    return render(request, template, context)

@login_required()
def submit_order(request):
    context = {}
    try:
        if request.method == 'POST':
            t = Territory.objects.get(code=request.POST.get('t_id'))
            f = Faction.objects.get(name=request.POST.get('f_id'))
            created = False
            try:
                a = Action.objects.get(territory=t, faction=f, turn=GameBoard.get_turn())
            except Action.DoesNotExist:
                a = Action(territory=t, faction=f, turn=GameBoard.get_turn())
                created = True
            a.type = request.POST.get('order_type')

            if a.type == MOVE:
                a.target = Territory.objects.get(code=request.POST.get('move_to'))
            elif a.type == SUPP:
                a.target = Territory.objects.get(code=request.POST.get('support_from'))
                a.support_type = request.POST.get('support_type')
                a.support_to = Territory.objects.get(code=request.POST.get('support_to'))
            elif a.type == SPEC:
                a.special = request.POST.get('special')
            else:
                a.target = None
            try:
                a.save()
            except Action.InvalidMoveError, e:
                context['status'] = 'iconized icon-error'

                context['message'] = 'Invalid move: %s ' % e.message
                return HttpResponse(json.dumps(context), mimetype="application/json")
            context['order'] = str(a)
            if created:
                context['message'] = 'Order created'
            else:
                context['status'] = 'iconized icon-ok-circle'
                context['message'] = 'Order accepted'

    except ValidationError, e:
        context['status'] = 'iconized icon-error'
        context['message'] = 'Invalid move: %s' % str(e.message_dict)
    except Exception, e:
        context['status'] = 'iconized icon-error'
        context['message'] = 'Server error: %s %s' % (e.message, type(e))
    return HttpResponse(json.dumps(context), mimetype="application/json")