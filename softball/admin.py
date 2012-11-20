from django.contrib import admin

from models import Team, Player, Game, Roster, Statistic


class GameStatisticAdmin(admin.TabularInline):
    model = Statistic
    fields = ('player', 'at_bats', 'runs', 'singles', 'doubles', 'triples',
              'home_runs', 'rbis', 'walks', 'strikeouts', )
    max_num = 12
    extra = 12


class PlayerStatisticAdmin(admin.TabularInline):
    model = Statistic
    fields = ('roster', 'at_bats', 'runs', 'singles', 'doubles', 'triples',
              'home_runs', 'rbis', 'walks', 'strikeouts', )
    extra = 3


class TeamAdmin(admin.ModelAdmin):
    search_fields = ('name', 'players__name', )


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'team', 'batting_average',
                    'on_base_percentage', 'slugging_percentage', 'at_bats',
                    'hits', 'runs', 'singles', 'doubles', 'triples',
                    'home_runs', 'rbis', 'walks', 'strikeouts', )
    search_fields = ('name', 'number', 'team__name', )
    list_filter = ('team', )
    readonly_fields = ('batting_average', 'on_base_percentage',
                       'slugging_percentage', 'at_bats', 'runs', 'singles',
                       'doubles', 'triples', 'home_runs', 'rbis', 'walks',
                       'strikeouts', )
    fieldsets = (
        (None, {
            'fields': ('name', 'number', 'team', )
        }),
        ('Performance', {
            'fields': ('batting_average', 'on_base_percentage',
                       'slugging_percentage', 'at_bats', 'runs', 'singles',
                       'doubles', 'triples', 'home_runs', 'rbis', 'walks',
                       'strikeouts', )
        }),
    )
    inlines = (PlayerStatisticAdmin, )


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'played_on', 'location', 'home_team', 'away_team',
                    'home_score', 'away_score', )
    search_fields = ('home_roster__team__name', 'away_roster__team__name',
                     'location', )
    list_filter = ('location', )
    ordering = ('played_on', )


    def home_team(self, obj):
        return obj.home_roster.team.name


    def away_team(self, obj):
        return obj.away_roster.team.name


class RosterAdmin(admin.ModelAdmin):
    list_display = ('team', 'home_game', 'away_game', )
    inlines = (GameStatisticAdmin, )


admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Roster, RosterAdmin)
