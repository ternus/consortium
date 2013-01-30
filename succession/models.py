# coding=utf-8
"""
Models for Line of Succession app
"""

from django.db import models
from gametex.models import GameTeXUser, GameTeXObject

ML=256

class Line(models.Model):
    name = models.CharField(max_length=ML)
    description = models.TextField(blank=True)
    members = models.ManyToManyField(GameTeXUser, through="LineOrder")
    ability_card = models.ForeignKey(GameTeXObject, blank=True, null=True)

    def __unicode__(self):
        return self.name

class LineOrder(models.Model):
    line = models.ForeignKey(Line)
    character = models.ForeignKey(GameTeXUser)
    order = models.PositiveSmallIntegerField()
    class Meta:
        ordering = ['order']
        unique_together = ('line', 'order')

    def __unicode__(self):
        return "%s %s %s" % (self.line, self.character.gto.name, self.order)