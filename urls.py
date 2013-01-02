from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html' }, name='home'),
    url(r'^403$', direct_to_template, { 'template': '403.html' }, name='403'),
    url(r'^404$', direct_to_template, { 'template': '404.html' }, name='404'),
    url(r'^500$', direct_to_template, { 'template': '500.html' }, name='500'),
    url(r'^index2/', 'project.views.index2', name='index2'),
    url(r'^contact/$', 'project.views.contact', name='contact'),
    url(r'^contact/complete/$', 'project.views.contact_complete',
        name='contact_complete'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^softball/', include('softball.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)

urlpatterns += staticfiles_urlpatterns()
