# Create your views here.
from django.shortcuts import render
from gametex.models import GTO

def keycard(request, template="keycards/show_keycard.html"):
    number = request.GET.get('number', None)
    found = False
    kc = None
    print number
    kcs = GTO.bc('KeyCard').filter(gametexfieldvalue__field__name='number',
                                       gametexfieldvalue__value=number)
    print kcs
    if kcs.exists():
        kc = kcs[0]
    context = {'found':found,
               'kc':kc,
               'number': number}
    return render(request, template, context)