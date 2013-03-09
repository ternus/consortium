# coding=utf-8
from django.conf.urls import patterns, include, url
from django.utils.translation import ugettext as _
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hexgrid2.views.home', name='home'),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'intro.html'}),
    url(r'^%s/' % _('market'), include('hexgrid.urls')),
    url(r'^gametex/', include('gametex_django_print.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^territory/', include('territory.urls')),
    url(r'^keycard/', include('keycards.urls')),
    url(r'^ask/', include('askgms.urls')),
    url(r'^mail/', include('messaging.urls')),
    url(r'^security/', include('security.urls')),
    url(r'^succession/', include('succession.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',  name='login' ),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='logout'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^c/', include('consortium.urls')),

)
