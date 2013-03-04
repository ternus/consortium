#coding=utf-8
"""
URL patterns for keycards.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'security.views.security', name='security'),
    url(r'^gm/$', 'security.views.gm_security', name='gm_security'),

)
