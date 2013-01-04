# coding=utf-8
from logging import log, debug
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
from django.shortcuts import get_object_or_404
from gametex.models import GameTeXObject
from hexgrid import config
from singleton_models.models import SingletonModel
from game_settings import *
from hexgrid.utils import get_currency

class Dir:
    """
    Multiple ways to represent hexagonal directions.
    """
    north, northeast, southeast, south, southwest, northwest = range(6)
    dirs = ("north", "northeast", "southeast", "south", "southwest","northwest")
    dirCaps = ("North", "Northeast", "Southeast", "South", "Southwest","Northwest")
    dabbrs = ("N", "NE", "SE", "S", "SW", "NW")

class Node(models.Model):
    """
    A single node in the hex grid.
    """
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=10)
    hex = models.IntegerField(unique=True, primary_key=True)
    quick_desc = models.CharField(max_length=256)
    dead_until_day = models.IntegerField(default=0)
    rumors_at_once = models.IntegerField(default=2)
    rumors_per_day = models.IntegerField(default=2)
    special = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    @classmethod
    def byHex(cls, hex):
        """
        @param hex Hex number to get.
        @return Hex or raises 404.
        """
        return get_object_or_404(Node, hex=hex)

    def neighbor(self, dir):
        """
        Get the hex in a direction, if it exists.

        @param dir Direction.
        @return Hex, or None.
        """
        try:
            if dir == Dir.north:
                node = Node.byHex(self.hex - 2)
            elif dir == Dir.northeast:
                node = Node.byHex(self.hex + 99 if self.hex % 2 else self.hex - 1)
            elif dir == Dir.southeast:
                node = Node.byHex(self.hex + 101 if self.hex % 2 else self.hex + 1)
            elif dir == Dir.south:
                node = Node.byHex(self.hex + 2)
            elif dir == Dir.southwest:
                node = Node.byHex(self.hex + 1 if self.hex % 2 else self.hex - 99)
            elif dir == Dir.northwest:
                node = Node.byHex(self.hex - 1 if self.hex % 2 else self.hex - 101)
            else:
                return None
            if not node.expired:
                return node
            else:
                return None
        except:
            return None

    def getAllNeighbors(self):
        """
        @return List of all neighbors.
        """
        neighbors = []
        for dir in range(6):
            q = self.neighbor(dir)
            if q:
                neighbors += [q]
        return neighbors

class Secret(models.Model):
    """
    A piece of info that may be revealed by providing the right password
    and paying the appropriate price.
    """
    node = models.ForeignKey(Node)
    password = models.CharField(max_length=256)
    moneycost = models.IntegerField(default=0, help_text="How much should the node charge to access the passtext?")
    othercost = models.TextField(blank=True, help_text="Any other price to see the secret (HTML OK)")
    text = models.TextField(help_text="What should the player see after successfully entering the password and meeting all costs?")
    valid = models.BooleanField(default=True)
    only_once = models.BooleanField(default=False, help_text="Should this secret only be accessible once?")

class Rumor(models.Model):
    """
    A rumor about a given subject.
    """
    subject = models.CharField(max_length=256, help_text="Who or what is the rumor about?")
    text = models.TextField(help_text="What should the player see after purchasing? (HTML OK)")
    probability = models.FloatField(default=1.0, help_text="How likely is this rumor to show up? (default 1.0; 2 is twice as likely, 0.5 is half as likely)")
    valid = models.BooleanField(default=True)

class NodeEvent(models.Model):
    """
    An event on a given node that might be seen by watchers.
    """
    where = models.ForeignKey(Node)
    when = models.DateTimeField(auto_now_add=True)
    who = models.ForeignKey("HGCharacter")
    who_disguised = models.BooleanField()
    what = models.CharField(max_length=256)
    day = models.IntegerField()

class Item(models.Model):
    """
    A thing for sale.  Can reference a GameTeXObject that meets item card constraints.
    """
    base_price = models.IntegerField(default=None, blank=True, null=True, help_text="Price for this item. Overrides the item card price, if applicable.")
    base_name = models.CharField(max_length=256, blank=True, help_text="Name for this item.  Overrides item card name.")
    post_buy = models.TextField("Post-buy text", blank=True, help_text="What should the player see after purchasing? (HTML OK, blank OK)")
    sold_by = models.ManyToManyField(Node, null=True, blank=True, verbose_name="Sold by", help_text="Who sells this?")
    item_card = models.ForeignKey(GameTeXObject, null=True, blank=True, verbose_name="Item card", help_text="Item card to sell. Can be null.<br \>"+
                                                                                          "Not seeing your item here? Make sure it has the %s field set." % PRICE_FIELD)

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
        return "%s (%s %s)" % (self.name, self.price, get_currency(self.price))

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
            x = self.name
        except AttributeError:
            raise ValidationError("You must either set the base name or link to an item card with a name.")
        try:
            x = self.price
        except AttributeError:
            raise ValidationError("You must either set the base price or link to an item card with a price.")

class CharNode(models.Model):
    """
    Links characters to nodes to track unlocking.
    """
    character = models.ForeignKey("HGCharacter")
    node = models.ForeignKey(Node)
    unlocked_on = models.IntegerField()

class CharNodeWatch(models.Model):
    """
    Links characters to nodes to track watchers.
    """
    char = models.ForeignKey("HGCharacter")
    node = models.ForeignKey(Node)
    watched_on = models.IntegerField()

class HGCharacter(models.Model):
    """
    HGCharacter ("Hex Grid Character")
    """
    user = models.OneToOneField(User)
    char = models.OneToOneField(GameTeXObject, blank=True)
    points = models.IntegerField()
    nodes = models.ManyToManyField(Node, through=CharNode)
    is_disguised = models.BooleanField()
    has_disguise = models.BooleanField()

    def all_nodes(self):
        """
        All nodes a character has unlocked.
        """
        return Node.objects.filter(id__in=CharNode.objects.filter(
            character=self).values_list('id', flat=True))

    def has_node(self, node):
        """
        Checks if a character has a node unlocked.
        """
        return CharNode.objects.filter(character=self, node=node).exists()

    def unlock_node_final(self, node):
        """
        Does *not* do error checking!
        """
        charnode = CharNode.objects.get_or_create(node=node, character=self)
        charnode.unlocked_on = GameDay.get_day()
        charnode.save()

        event = NodeEvent.objects.create(
            where = node,
            what = "unlocked",
            who = self,
            day = GameDay.get_day(),
            who_disguised = self.is_disguised,
        )
        event.save()



class GameDay(SingletonModel):
    """
    A singleton in the database keeping track of the game day.
    """
    day = models.IntegerField(default=0)
    tick_time = models.TimeField()

    @classmethod
    def get_day(cls):
        return cls.objects.get().day

    @classmethod
    def tick(cls):
        """
        Tick the game state forward one day.
        """
        for char in HGCharacter.objects.all():
            if char.char.has_field('market'):
                char.points = char.char.market
        gd = GameDay.objects.get()
        gd.day += 1
        gd.save()

        debug("TICK.  Day is now %d." % gd.day)