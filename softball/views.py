from django.template.response import TemplateResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import models

def team_list(request):
    """
    Lists all teams in the Database
    """
    paginator = Paginator(models.Team.objects.all().order_by('name'),
                          10)
    page = request.GET.get('page')
    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/team/list.html', {
        'teams': teams,
    })


def team_view(request, team_id):
    """
    Lists all teams in the Database
    """
    try:
        team = models.Team.objects.get(pk=team_id)
    except models.Team.DoesNotExist:
        raise Http404
    return TemplateResponse(request, 'softball/team/view.html', {
        'team': team,
        'record': team.record(),
    })


def player_list(request):
    """
    Lists all players in the Database
    """
    paginator = Paginator(models.Player.objects.all().order_by('name'), 
                          10)
    page = request.GET.get('page')
    try:
        players = paginator.page(page)
    except PageNotAnInteger:
        players = paginator.page(1)
    except EmptyPage:
        players = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/player/list.html', {
        'players': players,
    })


def game_list(request):
    """
    Lists all players in the Database
    """
    paginator = Paginator(models.Game.objects.all().order_by('played_on'), 
                          10)
    page = request.GET.get('page')
    try:
        games = paginator.page(page)
    except PageNotAnInteger:
        games = paginator.page(1)
    except EmptyPage:
        games = paginator.page(paginator.num_pages)
    return TemplateResponse(request, 'softball/game/list.html', {
        'games': games,
    })
