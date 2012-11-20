from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to


urlpatterns = patterns('',
    url(r'^$', redirect_to, { 'url': 'team', }, name='softball_home'),
    url(r'^team/$', 'softball.views.team_list', name='team_list'),
    url(r'^team/(?P<team_id>\d+)/$', 'softball.views.team_view', name='team_view'),
    url(r'^player/$', 'softball.views.player_list', name='player_list'),
)
