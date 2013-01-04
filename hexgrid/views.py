# coding=utf-8
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import  render, get_object_or_404, redirect
from hexgrid.models import Node, HGCharacter, Item, ForSale
from decorator import decorator
from django.utils.translation import ugettext as _, ungettext as _n

def gc(request):
    return get_object_or_404(HGCharacter, user=request.user)

@login_required()
def node(request, hex, template="node/node.html"):
    """
    Main view of a node.
    """
    node = Node.byHex(hex)
    context = {
        'node': node,
        'forsale': list(Item.objects.filter(sold_by=node)) + list(ForSale.objects.filter(sold_by=node)),
        'char': gc(request),
    }
    return render(request, template, context)

@login_required()
def unlock(request, hex, to_hex):
    char = gc(request)
    from_node = Node.byHex(hex)
    to_node = Node.byHex(to_hex)
    if not char.has_node(from_node):
        messages.error(request, "You didn't have node %s unlocked...?" % hex)
        return redirect('/')

    if char.has_node(to_node):
        messages.warning(request, "You already had node %s unlocked!" % to_hex)
        return node(request, to_hex)

    if not char.has

@login_required()
def node_map(request, template="node/node_map.html"):
    return render(request, template, {})

@login_required()
def buy(request, item_id, template="node/buy.html"):
    """
    Buy an item.
    """
    item = get_object_or_404(Item, id=item_id)

    result_str = _n("Congratulations!  You bought %(item)s for %(price)d %(currency_singular)s.",
                    "Congratulations!  You bought %(item)s for %(price)d %(currency_plural)s.",
                    item.price)

    added = (Item.item_card is not None)

    return render(request, template, {"result_str": result_str, "item": item})
