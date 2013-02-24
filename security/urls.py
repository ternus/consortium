#coding=utf-8
"""
URL patterns for keycards.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^security/$', 'security.views.security_window', name='security_window'),
    url(r'^entry/$', 'security.views.entry_window', name='entry_window'),
    url(r'^gm/$', 'security.views.gm_security', name='gm_security'),

)
