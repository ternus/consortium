# coding=utf-8
from logging import  debug
import random
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from gametex.models import GameTeXObject, GameTeXUser
import math
from singleton_models.models import SingletonModel
from hexgrid.game_settings import PRICE_FIELD, MARKET_STAT
from hexgrid.utils import currency
from django.utils.translation import ugettext as _


class Dir:
    """
    Multiple ways to represent hexagonal directions.
    """
    def __init__(self):
        pass

    north, northeast, southeast, south, southwest, northwest = range(6)
    dirs = ("north",
            "northeast",
            "southeast",
            "south",
            "southwest",
            "northwest")
    dirCaps = ("North",
               "Northeast",
               "Southeast",
               "South",
               "Southwest",
               "Northwest")
    dabbrs = ("N", "NE", "SE", "S", "SW", "NW")


class Node(models.Model):
    """
    A single node in the hex grid.
    """
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=10)
    hex = models.IntegerField(unique=True, primary_key=True)
    quick_desc = models.CharField(max_length=256)
    long_desc = models.TextField()
    dead_until_day = models.IntegerField(default=0)
    rumors_at_once = models.IntegerField(default=2)
    rumors_per_day = models.IntegerField(default=2)
    special = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    class Meta:
        ordering = ['hex']

    def __unicode__(self):
        return "%s [%s] <%s> %s" % (self.name, self.hex, self.short_name, self.quick_desc)

    width = 48
    scaling = 1

    def base_y(self):
        return (self.hex % 100) + (self.base_x() % 2) * .5

    def base_x(self):
        return (self.hex / 100)

    def x(self):
        return self.base_x() * (self.width * .75) * self.scaling - 650

    def y(self):
        return self.base_y() * (self.width * .86) * self.scaling - 400

    def points(self):
        # Points on a hex map
        x = float(self.x())
        y = float(self.y())
        sidelength = float(self.width / 2)
        xmotion = float(sidelength / 2)
        hexhalfheight = math.sin(math.radians(60))
        ymotion = sidelength * hexhalfheight

        sides = []
        sides.append([0, ymotion])
        sides.append([xmotion, 2 * ymotion])
        sides.append([xmotion + sidelength, 2 * ymotion])
        sides.append([sidelength * 2, ymotion])
        sides.append([xmotion + sidelength, 0])
        sides.append([xmotion, 0])

        return map(lambda s: [(s[0] + x), (s[1] + y)], sides)

    def pre_json(self):
        return {
            'name': self.name,
            'hex': self.hex,
            'points': self.points(),
            'short_name': self.short_name
        }


    @classmethod
    def by_hex(cls, hex_id):
        """
        @param hex_id Hex number to get.
        @return Hex or raises 404.
        """
        return get_object_or_404(Node, hex=hex_id)

    def neighbor(self, direction):
        """
        Get the hex in a direction, if it exists.

        @param direction Direction.
        @return Hex, or None.
        """

        try:
            _a = (self.hex / 100) % 2
            if direction == Dir.north:
                node = Node.objects.get(hex=(self.hex - 1))
            elif direction == Dir.northeast:
                node = Node.objects.get(hex=(self.hex + 100 if _a else self.hex + 99))
            elif direction == Dir.southeast:
                node = Node.objects.get(hex=(self.hex + 101 if _a else self.hex + 100))
            elif direction == Dir.south:
                node = Node.objects.get(hex=(self.hex + 1))
            elif direction == Dir.southwest:
                node = Node.objects.get(hex=(self.hex - 99 if _a else self.hex - 100))
            elif direction == Dir.northwest:
                node = Node.objects.get(hex=(self.hex - 100 if _a else self.hex - 101))
            else:
                return None
            if not node.expired:
                return node
            else:
                return None
        except Node.DoesNotExist:
            return None

    def get_all_neighbors(self):
        """
        @return List of all neighbors.
        """
        neighbors = []
        for direction in range(6):
            ngbr = self.neighbor(direction)
            if ngbr:
                neighbors += [ngbr]
        return neighbors

    def distance_to(self, node):
        distance = 0
        nodes = {self}

        while not node in nodes:
            for neighbors in map(lambda x: x.get_all_neighbors(), nodes):
                nodes.update(neighbors)
            distance += 1
            # print nodes
            if distance > Node.objects.all().count():
                return -1
        return distance

    def populate_rumors(self):
        pass

    @classmethod
    def populate_all_rumors(cls):
        """
        Set rumors for everyone.
        """
        for node in cls.objects.all():
            node.populate_rumors()

class Secret(models.Model):
    """
    A piece of info that may be revealed by providing the right password
    and paying the appropriate price.
    """
    node = models.ForeignKey(Node)
    password = models.CharField(max_length=256)
    moneycost = models.IntegerField(default=0,
        help_text="How much should the node charge to access the passtext?")
    othercost = models.TextField(blank=True,
        help_text="Any other price to see the secret (HTML OK)")
    text = models.TextField(
        help_text="What should the player see after successfully " + \
                  "entering the password and meeting all costs?")
    valid = models.BooleanField(default=True)
    only_once = models.BooleanField(default=False,
        help_text="Should this secret only be accessible once?")

class Rumor(models.Model):
    """
    A rumor about a given subject.
    """
    subject = models.CharField(max_length=256,
        help_text="Who or what is the rumor about?")
    text = models.TextField(
        help_text="What should the player see after purchasing? (HTML OK)")
    true = models.BooleanField(default=False)
    # quality = models.IntegerField(default=1, help_text="On a scale of 1-4, how good is this rumor?")
    valid = models.BooleanField(default=True)
#
class ItemBid(models.Model):
    character = models.ForeignKey("Character")
    item = models.ForeignKey("Item")
    node = models.ForeignKey("Node")
    amount = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    disguised = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    won = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s bid %s on %s (day %s)" % (self.character, self.amount, self.item, self.day)

EVENT_BUY      = "bought something"
EVENT_PASSWORD = "spoke a password"
EVENT_SECRET   = "heard a secret"
EVENT_RUMOR    = "heard a rumor"
EVENT_AGENT    = "placed an agent"
EVENT_BID      = "placed a bid"
EVENT_AUCTION  = "won an auction"
EVENT_UNLOCK   = "was introduced"
EVENT_UNLOCK_2 = "made an acquaintance"

EVENT_CHOICES = (
    (EVENT_BUY, EVENT_BUY),
    (EVENT_PASSWORD, EVENT_PASSWORD),
    (EVENT_AGENT, EVENT_AGENT),
    (EVENT_BID, EVENT_BID),
    (EVENT_AUCTION, EVENT_AUCTION),
    (EVENT_UNLOCK, EVENT_UNLOCK),
    (EVENT_SECRET, EVENT_SECRET),
    (EVENT_RUMOR, EVENT_RUMOR)
)


class NodeEvent(models.Model):
    """
    An event on a given node that might be seen by watchers.
    """
    where = models.ForeignKey(Node)
    when = models.DateTimeField(auto_now_add=True)
    who = models.ForeignKey("Character")
    who_disguised = models.BooleanField()
    type = models.CharField(max_length=20, choices=EVENT_CHOICES)
    day = models.IntegerField()
    item = models.ForeignKey("Item", null=True, blank=True)

    def __unicode__(self):
        return self.display_for(0, None)

    def display_for(self, distance, char):
        if char == self.who: distance = 0
        # random.seed(self.where.hex * distance * char.id * self.id)
        show = random.sample(["Where", "Who", "What"], 3 - distance)

        if self.who == char:
            who = "You"
        elif "Who" in show:
            who = "A mysterious figure" if self.who_disguised else self.who.name
        else:
            who = "Someone"

        if self.who == char and self.type == EVENT_UNLOCK:
            what = "were introduced to a merchant"
        elif "What" in show:
            what = self.type
        else:
            what = "did something"

        if "Where" in show:
            where = "at %s" % self.where.name
        else:
            where = "somewhere"
        return "%s %s %s." % (who, what, where)

RARITY_COMMON = "Common"
RARITY_RARE = "Rare"
RARITY_SCARCE = "Scarce"
RARITY_AUCTION = "Auction"

RARITY_CHOICES = (
    (RARITY_COMMON, "Common (price never changes)"),
    (RARITY_RARE, "Rare (price increases)"),
    (RARITY_SCARCE, "Scarce (chance item disappears)"),
    (RARITY_AUCTION, "Auction (only one, auction model)")
)

RARE_RANGE = 48 # Events in the last N hours increase rarity

class Item(models.Model):
    """
    A thing for sale.  Can reference a GameTeXObject that meets item card constraints.
    """
    base_price = models.IntegerField(default=None,
        blank=True,
        null=True,
        help_text="Price for this item. Overrides the item card price, " + \
                  "if applicable.")
    base_name = models.CharField(max_length=256,
        blank=True,
        help_text="Name for this item.  Overrides item card name.")
    post_buy = models.TextField("Post-buy text",
        blank=True,
        help_text="What should the player see after purchasing? " + \
                  "(HTML OK, blank OK)")
    rarity_class = models.CharField(max_length=10, choices=RARITY_CHOICES, default=RARITY_COMMON)
    rarity_prob = models.FloatField(default=0.0, help_text="For rare items, this is the factor by which the price increases: x * 2^(n * a), where x is the base price, n is the number of times bought, and a is this factor. For scarce items, this affects the probability it disappears (n rolls; if number less than a, item disappears).")
    sold_by = models.ManyToManyField(Node,
        null=True,
        blank=True,
        verbose_name="Sold by",
        help_text="Who sells this?")
    item_card = models.ForeignKey(GameTeXObject,
        null=True,
        blank=True,
        verbose_name="Item card",
        help_text="Item card to sell. Can be null.<br />"+
          "Not seeing your item here? Make sure it has the %s field set." \
          % PRICE_FIELD)
    valid = models.BooleanField(default=True, help_text="Goes False if the item disappears (sold or vanished if scarce)")

    @property
    def name(self):
        """
        Determine name of object, referencing item card if necessary.
        """
        if self.base_name:
            return self.base_name
        return self.item_card.name # May raise AttributeError.

    @property
    def initial_price(self):
        """
        Determine price of object, referencing item card if necessary.
        """
        if self.base_price:
            return self.base_price
        return int(self.item_card.get_field(PRICE_FIELD))

    @property
    def price(self):
        num_purchase_events = NodeEvent.objects.filter(day__gte=(GameDay.get_day() - 1), item=self).count()
        if self.rarity_class == RARITY_COMMON:
            return self.initial_price
        elif self.rarity_class == RARITY_RARE:
            return int(math.ceil(self.initial_price * (2 ** (num_purchase_events * self.rarity_prob))))
        elif self.rarity_class == RARITY_SCARCE:
            return self.initial_price
        elif self.rarity_class == RARITY_AUCTION:
            return -1
        else:
            return 0

    def __unicode__(self):
        return "%s" % (self.name)

    def __getattr__(self, item):
        try:
            return getattr(self.item_card, item)
        except:
            raise AttributeError

    def available(self):
        return self.valid

    def clean(self):
        """
        Validation method for the admin.
        """
        try:
            test = self.name
        except AttributeError:
            raise ValidationError("You must either set the base name " + \
            "or link to an item card with a name.")
        try:
            test = self.price
        except AttributeError:
            raise ValidationError("You must either set the base price " + \
            "or link to an item card with a price.")

class CharNode(models.Model):
    """
    Links characters to nodes to track unlocking.
    """
    character = models.ForeignKey("Character")
    node = models.ForeignKey(Node)
    unlocked_on = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s unlocked %s on day %s" % (self.character, self.node, self.unlocked_on)

class CharNodeWatch(models.Model):
    """
    Links characters to nodes to track watchers.
    """
    char = models.ForeignKey("Character")
    node = models.ForeignKey(Node)
    watched_on = models.IntegerField()

    def __unicode__(self):
        return "%s watching %s on %s" % (self.char, self.node, self.watched_on)

class Character(GameTeXUser):
    """
    Hex Grid Character")
    """
    phone = models.CharField(max_length=15, blank=True, default="")
    zephyr = models.CharField(max_length=8, blank=True, default="")
    contact_email = models.BooleanField(default=False)
    contact_zephyr = models.BooleanField(default=False)
    urgent_sms = models.BooleanField(default=True)
    routine_sms = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    nodes = models.ManyToManyField(Node, through=CharNode)
    is_disguised = models.BooleanField(default=False)
    has_disguise = models.BooleanField(default=False)
    alive = models.BooleanField(default=True)

    def __unicode__(self):
        return self.char.name

    @property
    def char(self):
        return self.gto

    @property
    def name(self):
        return self.char.name

    def all_nodes(self):
        """
        All nodes a character has unlocked.
        """
        return Node.objects.filter(id__in=CharNode.objects.filter(
            character=self).values_list('id', flat=True))

    def watched_nodes(self):
        """
        All nodes a character has unlocked.
        """
        return Node.objects.filter(id__in=CharNodeWatch.objects.filter(
            char=self).values_list('node', flat=True))

    def can_watch(self):
        return self.charnodewatch_set.all().count() <= self.market_stat()

    def visible_nodes(self):
        visible = set()
        for node in self.nodes.all():
            visible.update(node.get_all_neighbors())
        return Node.objects.filter(hex__in=map(lambda x: x.hex, visible))

    def unlockable_nodes(self):
        return self.visible_nodes().exclude(hex__in=map(lambda x: x.hex, self.nodes.all()))

    def has_node(self, node):
        """
        Checks if a character has a node unlocked.
        """
        return CharNode.objects.filter(character=self, node=node).exists()

    def watching_node(self, node):
        """
        Checks if a character has a node watched.
        """
        return CharNodeWatch.objects.filter(char=self, node=node).exists()

    def unlock_node_final(self, node):
        """
        Unlocks a node for a character.
        Does *not* do error checking!
        """
        charnode = CharNode.objects.get_or_create(node=node, character=self)[0]
        charnode.unlocked_on = GameDay.get_day()
        charnode.save()

        event = NodeEvent.objects.create(
            where = node,
            who = self,
            day = GameDay.get_day(),
            who_disguised = self.is_disguised,
            type = EVENT_UNLOCK
        )
        event.save()

    def watch_node_final(self, node):
        """
        Starts watching a node for a character.
        Does *not* do error checking!
        """
        watchnode = CharNodeWatch.objects.get_or_create(node = node,
            char = self,
            watched_on = GameDay.get_day())[0]
        watchnode.save()

        event = NodeEvent.objects.create(
            where=node,
            who=self,
            day=GameDay.get_day(),
            who_disguised=self.is_disguised,
            type=EVENT_AGENT
        )
        event.save()

    def unwatch_node_final(self, node):
        """
        Stops watching a node for a character.
        Does *not* do error checking!
        """
        CharNodeWatch.objects.get(node = node,
            char = self,
            watched_on = GameDay.get_day()).delete()

        NodeEvent.objects.filter(
            where=node,
            who=self,
            day=GameDay.get_day(),
            type=EVENT_AGENT
        ).all().delete()

    def bid_on(self, node, item, price):

        i = ItemBid.objects.get_or_create(
            node=node,
            item=item,
            character=self,
            day=GameDay.get_day(),
            disguised=self.is_disguised
        )[0]
        i.amount = price
        i.save()

        NodeEvent.objects.create(
            where=node,
            who=self,
            day=GameDay.get_day(),
            type=EVENT_BID,
            who_disguised=self.is_disguised
        )
        return i

    def revert_disguise(self, request):
        if self.is_disguised:
            self.is_disguised = False
            self.save()
            messages.warning(request, "Spent 1 Disguise; no longer disguised.")

    def market_stat(self):
        if not self.gto.has_field('Market'):
            return 0
        else:
            return int(self.gto.Market[0])

    def bid_for(self, item):
        pass

@receiver(post_save, sender=GameTeXUser)
def create_hgcharacter(sender, **kwargs):
    if kwargs['created']:
        g = kwargs['instance']
        h = Character(points = 0,#g.gto.field(MARKET_STAT, default=0),
        is_disguised = False,
        has_disguise = False)#(g.gto.field('disguise', default=0)))
        h.__dict__.update(g.__dict__)
        h.save()


class GameDay(SingletonModel):
    """
    A singleton in the database keeping track of the game day.
    """
    day = models.IntegerField(default=0)
    tick_time = models.TimeField()

    @classmethod
    def get_day(cls):
        """
        Get the game day.
        """
        return cls.objects.get().day

    @classmethod
    def tick(cls):
        """
        Tick the game state forward one day.
        """
        from messaging.models import Message

        # Resolve auctions.

        auctioned_items = Item.objects.filter(id__in=ItemBid.objects.filter(day=GameDay.get_day()).values('item'))

        for item in auctioned_items:
            bids = ItemBid.objects.filter(day=GameDay.get_day(), item=item, character__alive=True).order_by('-amount')
            winning = bids[0]
            winner = winning.character
            winning.won = True
            winning.resolved = True
            winning.save()
            NodeEvent.objects.create(
                where=winning.node,
                who=winner,
                day=GameDay.get_day(),
                type=EVENT_AUCTION,
                who_disguised=bids[0].disguised
            )

            Message.mail_to(winner, "Congratulations! You won %s!" % item.name,
                            "You've won %s at a cost of %s.<br />Here's what you've won:<br/><br/>%s"
                            % (item.name, winning.amount, item.post_buy), sender="Bakaara Market")
            losers = bids[1:]
            for loser in losers:
                loser.won = False
                loser.resolved = True
                loser.save()
                Message.mail_to(loser.character, "Sorry, you didn't win %s." % item.name,
                                "You didn't win %s.  Add %s back to your budget. Better luck next time!"
                                % (item.name, loser.amount), sender="Bakaara Market")
            item.valid = False
            item.save()

        for char in Character.objects.all():
            char.points = char.market_stat()
            char.save()

        for w in CharNodeWatch.objects.filter():
            messages = []
            events = {0:set(), 1:set(), 2:set()}
            for e in NodeEvent.objects.filter(where=w.node, day=GameDay.get_day()):
                events[0].update([e])
            nodes = set()
            for n in w.node.get_all_neighbors():
                for e in NodeEvent.objects.filter(where=n, day=GameDay.get_day()):
                    if not e in events[0]:
                        events[1].update([e])
                nodes.update(n.get_all_neighbors())
            for n in nodes:
                for e in NodeEvent.objects.filter(where=n, day=GameDay.get_day()):
                    if not e in events[0] or e in events[1]:
                        events[2].update([e])
            for ed in events:
                for e in events[ed]:
                    messages.append(e.display_for(ed, w.char))
            random.shuffle(messages)
            Message.mail_to(w.char, "Agent report from %s" % w.node.name,
                            "I saw the following things: <ul>" + "".join(("<li>%s</li>" % a) for a in messages) + "</ul>",
                            sender="Bakaara Market")

        for item in Item.objects.filter(valid=True):
            if item.rarity_class == RARITY_SCARCE:
                num_purchase_events = NodeEvent.objects.filter(day__gte=(GameDay.get_day() - 1), item=item).count()
                if num_purchase_events > 0:
                    if reduce(lambda a, b: a or b,
                              [random.random() < item.rarity_prob for _foo in range(num_purchase_events)],
                              False):  # Roll num_purchase_events random()s. If any come up True, item vanishes. So sad.
                        item.valid = False
                        item.save()

        gameday = GameDay.objects.get()
        gameday.day += 1
        gameday.save()

        debug("TICK.  Day is now %d." % gameday.day)