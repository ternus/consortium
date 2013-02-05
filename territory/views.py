# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from territory.models import Unit, Faction, Territory
from territory.somalia import somaliax as somalia_pts

@login_required()
def overview(request, faction_code, template="territory/territory.html"):
    somalia = ",".join(["[%s,%s]" %(x[0],x[1]) for x in Territory.convert_points(somalia_pts)])
    faction = get_object_or_404(Faction, code=faction_code)
    units = Unit.live_units().filter(faction=faction)
    territories = Territory.objects.all() #TODO can_see?
    context = {
        'somalia': somalia,
        'units':units,
        'territories': territories,
    }
    return render(request, template, context)