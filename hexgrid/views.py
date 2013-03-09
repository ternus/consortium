# coding=utf-8
"""
Views for hexgrid project.
"""
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import  render, get_object_or_404, redirect
from consortium.consortium import check_inspiration
from hexgrid.game_settings import CURRENCY_SINGULAR, CURRENCY_PLURAL, HOME_NODE
from hexgrid.models import Node, Character, Item, GameDay, CharNodeWatch, NodeEvent, Secret, ItemBid, RARITY_AUCTION, EVENT_BUY, EVENT_UNLOCK_2
from django.utils.translation import ugettext as _, ungettext as _n
from messaging.models import Message


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
    char = gtc(request)
    hex_node = Node.by_hex(hex_id)
    items = Item.objects.filter(sold_by=hex_node, valid=True)
    bids = {}
    for i in items:
        if i.rarity_class == RARITY_AUCTION:
            if ItemBid.objects.filter(character=char, item=i):
                bids[i] = ItemBid.objects.get(character=char, item=i).amount
    context = {
        'node': hex_node,
        'items': Item.objects.filter(sold_by=hex_node, valid=True),
        'bids': bids,
        'char': gtc(request),
        'game_day': GameDay.get_day(),
    }
    return render(request, template, context)

@login_required()
def toggle_disguise(request):
    char = gtc(request)
    char.is_disguised = not char.is_disguised
    char.save()
    if char.is_disguised:
        message = "You are now disguised."

    else:
        message = "You are no longer disguised."
    return HttpResponse(json.dumps({'message': message, 'disguise': char.is_disguised}), mimetype="application/json")

@login_required()
def unlock(request, from_hex, to_hex):
    """
    Unlock a node.  Does error checking.
    """
    char = gtc(request)
    from_node = Node.by_hex(from_hex)
    to_node = Node.by_hex(to_hex)
    print from_hex, HOME_NODE
    if not (char.has_node(from_node) or int(from_hex) == HOME_NODE):
        messages.error(request,
            _("You didn't have node %s unlocked...?") % from_hex)
        return home(request)

    if char.has_node(to_node):
        messages.warning(request,
            _("You already had node %s unlocked!") % to_hex)
        return redirect(node, to_hex)

    if char.points < 1:
        messages.error(request, _("You don't have any Market points!"))
        return redirect(node, from_hex)

    # Error checking done

    char.points -= 1
    char.save()

    char.unlock_node_final(to_node)
    event = NodeEvent.objects.create(
        where=from_node,
        who=char,
        day=GameDay.get_day(),
        who_disguised=char.is_disguised,
        type=EVENT_UNLOCK_2
    )

    char.revert_disguise(request)
    check_inspiration(request)

    messages.success(request,
        _("%(from_node_name)s introduces you to %(to_node_name)s." %
        {"from_node_name": from_node.name,
         "to_node_name": to_node.name}))

    return redirect(node, to_hex)

@login_required()
def node_password(request, from_hex, template="node/secret.html"):
    from_node = Node.by_hex(from_hex)
    password = request.GET.get("password", None)
    if Secret.objects.filter(node=from_node, password__iexact=password.strip()):
        s = Secret.objects.get(node=from_node, password__iexact=password.strip())
    else:
        s = None
    return render(request, template, {'node': from_node, 'secret': s})

@login_required()
def node_map(request, template="node/map.html"):
    """
    Generates a map of nodes the character has unlocked.
    """
    char = gtc(request)
    nodes = []
    unlockable = []
    if char:
        nodes = char.nodes.all()
        unlockable = char.unlockable_nodes()
    elif request.user.is_superuser:
        nodes = Node.objects.all()
    return render(request, template, {'nodes': json.dumps(map(lambda x: x.pre_json(), nodes)),
                                      'unlockable': json.dumps(map(lambda x: x.pre_json(), unlockable))})

@login_required()
def buy(request, node_hex, item_id, template="node/buy.html"):
    """
    Buy an item.
    """
    node = Node.by_hex(node_hex)
    char = gtc(request)
    item = get_object_or_404(Item, id=item_id)

    result_str = _n(
        "Congratulations! You bought %(item)s for %(price)d %(currency_singular)s.",
        "Congratulations! You bought %(item)s for %(price)d %(currency_plural)s.",
        item.price)

    result_str = result_str % {"item": item.name,
                               "price": item.price,
                               "currency_singular": CURRENCY_SINGULAR,
                               "currency_plural": CURRENCY_PLURAL}

    event = NodeEvent.objects.create(
         where=node,
         who=char,
         day=GameDay.get_day(),
         who_disguised=char.is_disguised,
         type=EVENT_BUY
     )

    char.revert_disguise(request)

    return render(request, template, {"result_str": result_str, "item": item, "node": node})

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

    char.revert_disguise(request)

    return redirect(node, hex_id)

@login_required()
def unwatch(request, from_hex, hex_id):
    """
    Remove a watcher from a node.
    """
    char = gtc(request)
    watch_node = Node.by_hex(hex_id)

    if not char.watching_node(watch_node):
        messages.error(request, _("You're not watching that node."))
        return node(request, hex_id)

    char.unwatch_node_final(watch_node)

    messages.success(request,
        _("You removed a watcher from %(node_name)s." %
        {"node_name": watch_node.name}))

    return redirect(node, from_hex) if from_hex else redirect(node, HOME_NODE)

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


def bid(request, hex, item):
    try:
        char = gtc(request)
        item = get_object_or_404(Item, id=item)
        node_hex = get_object_or_404(Node, hex=hex)
        amount = int(request.POST.get("amount", 0))
        bid_x = char.bid_on(node_hex, item, amount)
        messages.success(request, "Bid confirmed!")
        Message.mail_to(char, "Market Bid Confirmed", "Your bid of %s on %s has been confirmed. %s" % (amount, item, "You were disguised when you bid." if bid_x.disguised else ""), sender="Bakaara Market")
        char.revert_disguise(request)
    except Exception, e:
        messages.error(request, "Something went wrong and your bid was not processed: %s" % e.message)
    return redirect(node, hex)
