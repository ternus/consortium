# coding=utf-8

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^charlist/$', 'consortium.views.char_list', name='char_list'),
                       url(r'^profile/(\d+)/$', 'consortium.views.char_profile', name='char_profile'),

                       url(r'^prefs/(\d+)/$', 'consortium.views.char_prefs', name='char_prefs'),
                       )
