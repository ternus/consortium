# coding=utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'app.views.app', name='app'),
    url(r'^(?P<app_id>\w+)/$', 'app.views.app', name='app')

)