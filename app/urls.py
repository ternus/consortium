# coding=utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'app.views.app', name='app'),
    url(r'^csv/$', 'app.views.app_csv', name='app_csv'),
    url(r'^dashboard/$', 'app.views.dashboard', name='dashboard'),
    url(r'^remind/(?P<app_id>\w+)/$', 'app.views.remind', name='remind'),
    url(r'^remind_everyone/$', 'app.views.remind_everyone', name='remind_everyone'),

    url(r'^(?P<app_id>\w+)/$', 'app.views.app', name='app'),
)