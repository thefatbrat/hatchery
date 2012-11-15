from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, { 'template': 'index.html' }, name='home'),
    url(r'^index2/', 'project.views.index2', name='index2'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^softball/', include('softball.urls')),
)
