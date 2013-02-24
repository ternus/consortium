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

    def current_leader(self):
        if self.lineorder_set.order_by('order').exists():
            return self.lineorder_set.order_by('order')[0]
        return None

    @classmethod
    def by_char(cls, hgc, **kwargs):
        return cls.objects.filter(lineorder__character=hgc, lineorder__order=1)

class LineOrder(models.Model):
    line = models.ForeignKey(Line)
    character = models.ForeignKey(GameTeXUser)
    order = models.PositiveSmallIntegerField()
    class Meta:
        ordering = ['order']
        unique_together = ('line', 'order')

    def __unicode__(self):
        return "%s %s %s" % (self.line, self.character.gto.name, self.order)