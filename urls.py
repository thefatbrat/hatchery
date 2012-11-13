from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, { 'template': 'index5.html' }, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^softball/', include('softball.urls')),
    url(r'^index2/', 'project.views.index2', name='index2'),
)
