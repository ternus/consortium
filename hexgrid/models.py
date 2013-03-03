# coding=utf-8
from logging import  debug
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
    probability = models.FloatField(default=1.0,
        help_text="How likely is this rumor to show up?" + \
                  " (default 1.0; 2 is twice as likely, 0.5 is half as likely)")
    # quality = models.IntegerField(default=1, help_text="On a scale of 1-4, how good is this rumor?")
    valid = models.BooleanField(default=True)

class ItemBid(models.Model):
    character = models.ForeignKey("Character")
    item = models.ForeignKey("Item")
    day = models.IntegerField(default=0)
    resolved = models.BooleanField(default=False)
    won = models.BooleanField(default=False)

class NodeEvent(models.Model):
    """
    An event on a given node that might be seen by watchers.
    """
    where = models.ForeignKey(Node)
    when = models.DateTimeField(auto_now_add=True)
    who = models.ForeignKey("Character")
    who_disguised = models.BooleanField()
    what = models.CharField(max_length=256)
    day = models.IntegerField()

RARITY_CHOICES = (
    (0, "Common (price never changes)"),
    (1, "Rare (price increases over time)"),
    (2, "Scarce (chance item disappears)"),
    (3, "Unique (only one)"),
    (4, "Auction (only one, auction model)")
)

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

    @property
    def name(self):
        """
        Determine name of object, referencing item card if necessary.
        """
        if self.base_name:
            return self.base_name
        return self.item_card.name # May raise AttributeError.

    @property
    def price(self):
        """
        Determine price of object, referencing item card if necessary.
        """
        if self.base_price:
            return self.base_price
        return int(self.item_card.get_field(PRICE_FIELD))

    def __unicode__(self):
        return "%s (%s)" % (self.name, currency(self.price))

    def __getattr__(self, item):
        try:
            return getattr(self.item_card, item)
        except:
            raise AttributeError

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

class CharNodeWatch(models.Model):
    """
    Links characters to nodes to track watchers.
    """
    char = models.ForeignKey("Character")
    node = models.ForeignKey(Node)
    watched_on = models.IntegerField()

class Character(GameTeXUser):
    """
    Hex Grid Character")
    """
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
            character=self).values_list('id', flat=True))

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
        return CharNodeWatch.objects.filter(character=self, node=node).exists()

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
            what = _("unlocked"),
            who = self,
            day = GameDay.get_day(),
            who_disguised = self.is_disguised,
        )
        event.save()

    def watch_node_final(self, node):
        """
        Starts watching a node for a character.
        Does *not* do error checking!
        """
        watchnode = CharNodeWatch.objects.get_or_create(node = node,
            character = self,
            watched_on = GameDay.get_day())[0]
        watchnode.save()

        event = NodeEvent.objects.create(
            where=node,
            what=_("watched"),
            who=self,
            day=GameDay.get_day(),
            who_disguised=self.is_disguised,
        )
        event.save()

    def unwatch_node_final(self, node):
        """
        Stops watching a node for a character.
        Does *not* do error checking!
        """
        CharNodeWatch.objects.get(node = node,
            character = self,
            watched_on = GameDay.get_day()).delete()

        NodeEvent.objects.get(
            where=node,
            what=_("watched"),
            who=self,
            day=GameDay.get_day(),
        ).delete()
#
# @receiver(post_save, sender=Character)
# def create_mailbox(sender, **kwargs):
#     from messaging.models import Mailbox
#     if kwargs['created']:
#         print kwargs['instance']
#         Mailbox.objects.get_or_create(name=kwargs['instance'].name,
#                                       type=2)

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
        for char in Character.objects.all():
            if char.char.has_field('market'):
                char.points = char.char.market

        for node in Node.objects.all():
            pass
        gameday = GameDay.objects.get()
        gameday.day += 1
        gameday.save()

        debug("TICK.  Day is now %d." % gameday.day)