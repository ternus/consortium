#coding=utf-8
"""
URL patterns for hexgrid.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'succession.views.my_lines', name='my_lines'),
    url(r'^gm/$', 'succession.views.gm_lines', name='gm_lines'),
    url(r'^gm/kill/$', 'succession.views.kill_character', name='kill_character'),
    url(r'^line/(\d+)/$', 'succession.views.show_line', name='show_line'),

)
