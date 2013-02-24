# coding=utf-8
"""
Views for hexgrid project.
"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import  render, get_object_or_404, redirect
from hexgrid.game_settings import CURRENCY_SINGULAR, CURRENCY_PLURAL, HOME_NODE
from hexgrid.models import Node, Character, Item, GameDay, CharNodeWatch, NodeEvent
from django.utils.translation import ugettext as _, ungettext as _n

def gtc(request):
    """
    Shortcut method to get a HexGridCharacter from request.user
    """
    try:
        return Character.objects.get(user=request.user)
    except:
        return None
#    return get_object_or_404(Character, user=request.user)

@login_required()
def home(request):
    """
    Default view for /
    """
    return redirect(node, HOME_NODE)

@login_required()
def node(request, hex_id, template="node/node.html"):
    """
    Main view of a node.
    """
    hex_node = Node.by_hex(hex_id)
    print gtc(request)
    context = {
        'node': hex_node,
        'items': Item.objects.filter(sold_by=hex_node),
        'char': gtc(request),
        'game_day': GameDay.get_day(),
    }
    return render(request, template, context)

@login_required()
def unlock(request, from_hex, to_hex):
    """
    Unlock a node.  Does error checking.
    """
    char = gtc(request)
    from_node = Node.by_hex(from_hex)
    to_node = Node.by_hex(to_hex)
    if not char.has_node(from_node):
        messages.error(request,
            _("You didn't have node %s unlocked...?") % from_hex)
        return home(request)

    if char.has_node(to_node):
        messages.warning(request,
            _("You already had node %s unlocked!") % to_hex)
        return redirect(node, to_hex)

    if not char.points:
        messages.error(request, _("You don't have any Market points!"))
        return redirect(node, from_hex)

    # Error checking done

    char.unlock_node_final(to_node)

    messages.success(request,
        _("%(from_node_name)s introduces you to %(to_node_name)s." %
        {"from_node_name": from_node.name,
         "to_node_name": to_node.name}))

    return redirect(node, to_hex)

@login_required()
def node_map(request, template="node/node_map.html"):
    """
    Generates a map of nodes the character has unlocked.
    """
    return render(request, template, {})

@login_required()
def buy(request, item_id, template="node/buy.html"):
    """
    Buy an item.
    """
    item = get_object_or_404(Item, id=item_id)

    result_str = _n(
        "Congratulations! You bought %(item)s for %(price)d %(currency_singular)s.",
        "Congratulations! You bought %(item)s for %(price)d %(currency_plural)s.",
        item.price)

    result_str = result_str % {"item": item.name,
                               "price": item.price,
                               "currency_singular": CURRENCY_SINGULAR,
                               "currency_plural": CURRENCY_PLURAL}



    #added = (Item.item_card is not None)

    return render(request, template, {"result_str": result_str, "item": item})

@login_required()
def watch(request, hex_id):
    """
    Put a "watcher" on a node that looks for what happens nearby.
    """
    char = gtc(request)
    watch_node = Node.by_hex(hex_id)

    if not char.has_node(watch_node):
        messages.error(request, _("You haven't unlocked that node."))
        return node(request, hex_id)

    if char.watching_node(watch_node):
        messages.warning(request, _("You're already watching that node."))
        return node(request, hex_id)

    char.watch_node_final(watch_node)

    messages.success(request,
        _("You put a watcher near %(node_name)s." %
        {"node_name": watch_node.name}))

    return node(request, hex_id)

@login_required()
def unwatch(request, hex_id):
    """
    Remove a watcher from a node.
    """
    char = gtc(request)
    watch_node = Node.by_hex(hex_id)

    if not char.watching_node(watch_node):
        messages.error(request, _("You're not watching that node."))
        return node(request, hex_id)

    char.watch_node_final(watch_node)

    messages.success(request,
        _("You put a watcher near %(node_name)s." %
        {"node_name": watch_node.name}))

    return node(request, hex_id)

@login_required()
def events(request, template="node/events.html"):
    """
    View events that you saw.
    """
    char = gtc(request)

    days = range(GameDay.get_day() - 1)

    events = []

    for day in days:
        day_events = []
        for watch in CharNodeWatch.objects.filter(char=char, day=day):
            watch_events = NodeEvent.objects.filter(
                where=watch.node,
                day=day
                )
            day_events.append(watch_events)
        events.append(day_events)

    return render(request, template, {"events": events})