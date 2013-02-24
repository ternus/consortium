#coding=utf-8
"""
URL patterns for hexgrid.
"""
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'territory.views.overview', name='overview'),
    url(r'^orders/(?P<faction_code>\w+)/(?P<turn>\d+)/$', 'territory.views.orders_json', name='orders_json'),

    url(r'^gm/$', 'territory.views.gm_overview', name='gm_overview'),
    url(r'^gm/orders/(?P<turn>\d+)/$', 'territory.views.orders_json', name='gm_orders_json'),
    url(r'^gm/tick/$', 'territory.views.game_tick', name='game_tick'),

    url(r'^submit/$', 'territory.views.submit_order', name='submit_order'),

#    url(r'^(?P<faction_code>\w+)/$', 'territory.views.overview', name='overview'),
#    url(r'^line/(\d+)/$', 'succession.views.show_line', name='show_line'),

)
