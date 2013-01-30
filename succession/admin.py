# coding=utf-8
from django.contrib import admin
from models import Line, LineOrder

class LineOrderInline(admin.TabularInline):
    model = LineOrder

class LineAdmin(admin.ModelAdmin):
    inlines = (LineOrderInline,)

admin.site.register(Line, LineAdmin)