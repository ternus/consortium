#coding=utf-8
"""
URL patterns for keycards.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'messaging.views.mail_home', name='mail_home'),
    url(r'^gm/$', 'messaging.views.gm_mail_home', name='gm_mail_home'),
    url(r'^set_read/$', 'messaging.views.set_read', name='set_read'),

)
