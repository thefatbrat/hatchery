from django.template.response import TemplateResponse

import models

def team_list(request):
    """
    Lists all teams in the Database
    """
    teams = models.Team.objects.all().order_by('name')
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
    Lists all teams in the Database
    """
    return TemplateResponse(request, 'softball/player/list.html', {
        'players': models.Player.objects.all(),
    })
