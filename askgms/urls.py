# coding=utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'askgms.views.player_view', name='askgms'),
    url(r'^gm/$', 'askgms.views.gm_view', name='askgms_gm'),
)