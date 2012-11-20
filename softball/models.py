import django.db.models

import calc


class Team(django.db.models.Model):
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)
    name = django.db.models.CharField(max_length=150, db_index=True)


    def __unicode__(self):
        return self.name


    def record(self):
        wins = [r.game().winner==self for r in self.rosters.all()]
        return wins.count(True), wins.count(False)

class Player(django.db.models.Model):
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)
    name = django.db.models.CharField(max_length=150, unique=True)
    number = django.db.models.PositiveIntegerField()
    team = django.db.models.ForeignKey('Team', related_name='players')

    class Meta:
        ordering = ["name", ]

    def __unicode__(self):
        return u'{0} #{1} - {2}'.format(self.name,
                                        self.number or 'N/A',
                                        self.team.name)


    def at_bats(self):
        """
        Returns the total number of at_bats for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('at_bats'))['s'] or 0
    at_bats.short_description = u'AB'


    def hits(self):
        """
        Returns the total singles, doubles, triples, and home_runs
        """
        return sum(filter(None,
            self.statistics.aggregate(django.db.models.Sum('singles'),
                                      django.db.models.Sum('doubles'),
                                      django.db.models.Sum('triples'),
                                      django.db.models.Sum('home_runs')
            ).values()))
    hits.short_description = u'H'


    def walks(self):
        """
        Returns the total number of walks for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('walks'))['s'] or 0
    walks.short_description = u'BB'


    def strikeouts(self):
        """
        Returns the total number of strikeouts for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('strikeouts'))['s'] or 0
    strikeouts.short_description = u'K'


    def runs(self):
        """
        Returns the total number of runs for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('runs'))['s'] or 0
    runs.short_description = u'R'


    def singles(self):
        """
        Returns the total number of singles for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('singles'))['s'] or 0
    singles.short_description = u'1B'


    def doubles(self):
        """
        Returns the total number of doubled for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('doubles'))['s'] or 0
    doubles.short_description = u'2B'


    def triples(self):
        """
        Returns the total number of triples for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('triples'))['s'] or 0
    triples.short_description = u'3B'


    def home_runs(self):
        """
        Returns the total number of home runs for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('home_runs'))['s'] or 0
    home_runs.short_description = u'HR'


    def rbis(self):
        """
        Returns the total number of rbis for this player
        """
        return self.statistics.aggregate(
            s=django.db.models.Sum('rbis'))['s'] or 0
    rbis.short_description = u'RBI'


    def batting_average(self):
        if self.hits() > self.at_bats():
            return 0
        return calc.average(self.at_bats(), self.hits())
    batting_average.short_description = u'AVG'


    def on_base_percentage(self):
        if self.hits() > self.at_bats():
            return 0
        return calc.on_base_percentage(
            self.at_bats(), self.walks(), self.hits())
    on_base_percentage.short_description = u'OB%'

    def slugging_percentage(self):
        if self.hits() > self.at_bats():
            return 0
        return calc.slugging_percentage(self.at_bats(), self.singles(),
                                        self.doubles(), self.triples(),
                                        self.home_runs())
    slugging_percentage.short_description = u'SLG%'


class Game(django.db.models.Model):
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)
    played_on = django.db.models.DateTimeField()
    location = django.db.models.CharField(max_length=150)
    home_roster = django.db.models.OneToOneField('Roster',
                                                 related_name='home_game')
    away_roster = django.db.models.OneToOneField('Roster',
                                                 related_name='away_game')


    def __unicode__(self):
        return u'{0} - {1}'.format(self.location, self.played_on)


    @property
    def winner(self):
        if self.away_score > self.home_score:
            return self.away_roster.team
        else:
            return self.home_roster.team


    @property
    def final_score(self):
        """
        Returns the final score of the game, as recorded in the rosters, as a
        tuple (away_score, home_score)
        """
        return self.away_score, self.home_score


    @property
    def home_score(self):
        """
        Returns the score of the home team, as recorded in the home roster
        """
        return self.home_roster.player_statistics.aggregate(
            s=django.db.models.Sum('runs'))['s'] or 0


    @property
    def away_score(self):
        """
        Returns the score of the home team, as recorded in the home roster
        """
        return self.away_roster.player_statistics.aggregate(
            s=django.db.models.Sum('runs'))['s'] or 0


class Roster(django.db.models.Model):
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)
    team = django.db.models.ForeignKey('Team', related_name='rosters')


    def __unicode__(self):
        return '{0} - {1}'.format(self.team.name, self.id)


    def game(self):
        try:
            return self.home_game
        except Game.DoesNotExist:
            return self.away_game


class Statistic(django.db.models.Model):
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)
    player = django.db.models.ForeignKey('Player', related_name='statistics')
    at_bats = django.db.models.PositiveIntegerField(u'AB', default=0)
    runs = django.db.models.PositiveIntegerField('R', default=0)
    singles = django.db.models.PositiveIntegerField('1B', default=0)
    doubles = django.db.models.PositiveIntegerField('2B', default=0)
    triples = django.db.models.PositiveIntegerField('3B', default=0)
    home_runs = django.db.models.PositiveIntegerField('HR', default=0)
    rbis = django.db.models.PositiveIntegerField('RBI', default=0)
    walks = django.db.models.PositiveIntegerField('BB', default=0)
    strikeouts = django.db.models.PositiveIntegerField('K', default=0)
    roster = django.db.models.ForeignKey('Roster',
                                         related_name='player_statistics')


    def __unicode__(self):
        return u'{name} ({roster_id}): AB:{at_bats} R:{runs} 1B:{singles} ' \
               u'2B:{doubles} 3B:{triples} HR:{home_runs} RBI:{rbis} ' \
               u'BB:{walks} K:{strikeouts}'.format(
            name=self.player.name, roster_id=self.roster_id,
            at_bats=self.at_bats, runs=self.runs, singles=self.singles,
            doubles=self.doubles, triples=self.triples,
            home_runs=self.home_runs, walks=self.walks,
            strikeouts=self.strikeouts, rbis=self.rbis)


    @property
    def hits(self):
        return self.singles + self.doubles + self.triples + self.home_runs


    @property
    def batting_average(self):
        if self.hits > self.at_bats:
            return 0
        return calc.average(self.at_bats, self.hits)
