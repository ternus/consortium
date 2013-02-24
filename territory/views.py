# Create your views here.
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from hexgrid.models import Character
from hexgrid.views import gtc
from succession.models import Line
from territory.models import Unit, Faction, Territory, Action, GameBoard, validation_str, SPEC, SUPP, MOVE
from territory.somalia import somaliax as somalia_pts


def get_orders(faction_code=None, turn=None):
    if not turn: turn=GameBoard.get_turn()
    actions = Action.objects.filter(turn=turn)
    if faction_code:
        actions = actions.filter(faction__code=faction_code)

    orders = {}

    for a in actions:
        orders[a.territory.code] = {
            'gm_str': str(a),
            'time': str(a.time),
            'str': a.p_str,
            'faction': a.faction.code,
            'turn': a.turn,
            'territory': a.territory.code,
            'type': a.type,
            'target': a.target.code,
            'special': a.special,
            'issuer': a.issuer.gto.name if a.issuer else None,
            'support_type': a.support_type,
            'support_to': a.support_to.code if a.support_to else None,
            'validation_level': validation_str(a.validation_level)
        }
    return orders

@login_required()
def orders_json(request, faction_code=None, turn=None):
    context = {
        'orders': get_orders(faction_code, turn)
    }
    return HttpResponse(json.dumps(context), mimetype="application/json")

@login_required()
def overview(request, template="territory/territory.html"):
    somalia = ",".join(["[%s,%s]" % (x[0], x[1]) for x in Territory.convert_points(somalia_pts)])
    user = gtc(request)
    faction_code = Line.objects.filter(lineorder__order=1, lineorder__character=user).exclude(faction=None).faction
    faction = get_object_or_404(Faction, code=faction_code)
    #    units = Unit.live_units().filter(faction=faction)
    territories = Territory.objects.all()
    context = {
        'faction': faction,
        'w_turn': GameBoard.get_turn(),
        'last_w_turn': GameBoard.get_turn()-1, #ugh
        'orders': json.dumps(get_orders(faction.code)),
        'somalia': somalia,
        'territories': territories,
    }
    return render(request, template, context)


@login_required()
def gm_overview(request, template="territory/territory.html"):
    if not request.user.is_superuser: raise Http404
    somalia = ",".join(["[%s,%s]" % (x[0], x[1]) for x in Territory.convert_points(somalia_pts)])
    territories = Territory.objects.all()
    context = {
        'orders': json.dumps(get_orders()),
        'somalia': somalia,
        'w_turn': GameBoard.get_turn(),
        'last_w_turn': GameBoard.get_turn() - 1, #ugh
        'territories': territories,
    }
    return render(request, template, context)


@login_required()
def game_tick(request):
    if not request.user.is_superuser: raise Http404

    GameBoard.objects.get().execute_turn()
    messages.success(request, 'Done! It is now turn %s' % GameBoard.get_turn())

    return redirect(gm_overview)

@login_required()
def submit_order(request):
    context = {}
    try:
        if request.method == 'POST':
            print request.POST
            if request.POST.get('gm_sekrit', False):
                c = None
            else:
                c = Character.objects.get(id=request.POST.get('u_id'))
            t = Territory.objects.get(code=request.POST.get('t_id'))
            f = Faction.objects.get(name=request.POST.get('f_id'))
            if t.owner != f:
                context['status'] = 'iconized icon-error'
                context['message'] = "Can't issue order for territory not yours"
                return HttpResponse(json.dumps(context), mimetype="application/json")

            created = False
            try:
                a = Action.objects.get(territory=t, faction=f, turn=GameBoard.get_turn())
            except Action.DoesNotExist:
                a = Action(territory=t, faction=f, turn=GameBoard.get_turn())
                created = True
            a.type = request.POST.get('order_type')
            if c:
                a.issuer = c

            if a.type == MOVE:
                a.target = Territory.objects.get(code=request.POST.get('move_to'))
            elif a.type == SUPP:
                a.target = Territory.objects.get(code=request.POST.get('support_from'))
                a.support_type = request.POST.get('support_type')
                if a.support_type == MOVE:
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