#coding=utf-8
"""
URL patterns for hexgrid.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'territory.views.overview', name='overview'),

#    url(r'^(?P<faction_code>\w+)/$', 'territory.views.overview', name='overview'),
#    url(r'^line/(\d+)/$', 'succession.views.show_line', name='show_line'),

)
