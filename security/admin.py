# coding=utf-8
from django.contrib import admin
from security.models import SecureLocation, EntryWindow, SecurityWindow
from territory.models import Territory, Faction, Action, Unit

admin.site.register(SecureLocation)
admin.site.register(EntryWindow)
admin.site.register(SecurityWindow)