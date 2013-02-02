#coding=utf-8
"""
URL patterns for keycards.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'keycards.views.keycard', name='keycard'),
)
