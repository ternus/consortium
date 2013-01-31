#encoding=utf-8

from django.template.defaulttags import register

@register.filter
def lookup(d, key):
    return d.get(key)
