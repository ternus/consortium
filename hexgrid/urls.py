#coding=utf-8
"""
URL patterns for hexgrid.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'hexgrid.views.home', name='home'),
    url(r'^node/(\d+)/$', 'hexgrid.views.node', name='node'),
    url(r'^unlock/(\d+)/(\d+)/$', 'hexgrid.views.unlock', name='unlock'),
    url(r'^watch/(\d+)/$', 'hexgrid.views.watch', name='watch'),
    url(r'^buy/(\d+)/$', 'hexgrid.views.buy', name='buy'),
)
