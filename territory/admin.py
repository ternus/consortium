# coding=utf-8
from django.contrib import admin
from territory.models import Territory, Faction, Action, Unit

admin.site.register(Territory)
admin.site.register(Faction)
admin.site.register(Action)
admin.site.register(Unit)
