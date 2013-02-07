# Create your views here.
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from territory.models import Unit, Faction, Territory, Action, GameBoard
from territory.somalia import somaliax as somalia_pts

@login_required()
def overview(request, template="territory/territory.html"):
    somalia = ",".join(["[%s,%s]" %(x[0],x[1]) for x in Territory.convert_points(somalia_pts)])
#    faction = get_object_or_404(Faction, code=faction_code)
#    units = Unit.live_units().filter(faction=faction)
    territories = Territory.objects.all() #TODO can_see?
    context = {
        'somalia': somalia,
        'territories': territories,
    }
    return render(request, template, context)

@login_required()
def submit_order(request):
    context = {}
    try:
        if request.method == 'POST':
            t = Territory.objects.get(id=request.POST.get('territory_id'))
            a = Action.objects.get_or_create(territory=t, turn=GameBoard.get_turn())[0]
            a.type = request.POST.get('order_type')
            try:
                a.save()
            except ValidationError, e:
                context['status'] = 'Error: %s ' %e.message
            context['status'] = 'Order submitted'
    except:
        context['status'] = 'invalid'
    return HttpResponse(json.dumps(context), mimetype="application/json")