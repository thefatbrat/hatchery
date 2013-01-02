from django.forms import Form, ModelForm, ModelChoiceField, PasswordInput
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import models


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', )


class UserSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', )


class TeamForm(ModelForm):
    error_css_class = 'text-error'
    required_css_class = 'text-required'

    class Meta:
        model = models.Team
        exclude = ('owned_by', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TeamForm, self).__init__(*args, **kwargs)


class PlayerForm(ModelForm):
    error_css_class = 'text-error'
    required_css_class = 'text-required'

    class Meta:
        model = models.Player
        exclude = ('owned_by', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields['team'].queryset = self.user.teams.all()


class GameForm(ModelForm):
    away_team = ModelChoiceField(label=u'Away Team',
                                 required=True,
                                 queryset=models.Team.objects.all(),
                                 help_text=u'Changing the team will clear the '
                                           u'roster')
    home_team = ModelChoiceField(label=u'Home Team',
                                 required=True,
                                 queryset=models.Team.objects.all(),
                                 help_text=u'Changing the team will clear the '
                                           u'roster')
    error_css_class = 'text-error'
    required_css_class = 'text-required'

    class Meta:
        model = models.Game
        fields = ('played_on', 'location', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['home_team'].queryset = models.Team.objects.filter(
            owned_by=user)
        self.fields['away_team'].queryset = models.Team.objects.filter(
            owned_by=user)

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('home_team') == cleaned_data.get('away_team') and\
                cleaned_data['home_team']:
            msg = u'Home team and Away team cannot be the same.'
            self._errors['home_team'] = self.error_class([msg])
            self._errors['away_team'] = self.error_class([msg])
            # These fields are no longer valid. Remove them from the
            # cleaned data.
            del cleaned_data['home_team']
            del cleaned_data['away_team']
        return cleaned_data

    def save(self, commit=True):
        game = super(GameForm, self).save(commit=False)
        game.owned_by = self.user
        if commit:
            game.save()
        return game


class TeamPlayerForm(ModelForm):
    class Meta:
        model = models.Player
        exclude = ('owned_by', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # accept a Team to use for Player selection
        super(TeamPlayerForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        player = super(TeamPlayerForm, self).save(commit=False)
        player.owned_by = self.user
        if commit:
            player.save()
        return player


class TeamPlayerFormSet(BaseInlineFormSet):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(TeamPlayerFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, index, **kwargs):
        # override _construct_form to add self.team to the StatisticForm upon
        # creation
        kwargs['user'] = self.user
        return super(TeamPlayerFormSet, self)._construct_form(index, **kwargs)


TeamPlayerModelFormSet = inlineformset_factory(
    parent_model=models.Team, model=models.Player, formset=TeamPlayerFormSet,
    form=TeamPlayerForm, extra=20, max_num=20)


class StatisticForm(ModelForm):
    class Meta:
        model = models.Statistic
        exclude = ('owned_by', )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        # accept a Team to use for Player selection
        super(StatisticForm, self).__init__(*args, **kwargs)
        widget_overrides = (
            'at_bats', 'runs', 'singles', 'doubles', 'triples', 'home_runs',
            'rbis', 'walks', 'strikeouts',
        )
        # override the class of the widget_overrides fields
        for s in widget_overrides:
            self.fields[s].widget.attrs['class'] = 'input-mini right'

    def save(self, commit=True):
        statistic = super(StatisticForm, self).save(commit=False)
        statistic.owned_by = self.user
        if commit:
            statistic.save()
        return statistic


class GameStatisticForm(StatisticForm):
    def __init__(self, user, team, *args, **kwargs):
        self.user = user
        self.team = team
        super(GameStatisticForm, self).__init__(user, *args, **kwargs)
        # use the team to override the players field queryset
        self.fields['player'].queryset = self.team.players.all()


class GameStatisticFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(GameStatisticFormSet, self).__init__(*args, **kwargs)
        if 'queryset' not in kwargs:
            kwargs['queryset'] = self.instance.player_statistics.all()

    def _construct_form(self, index, **kwargs):
        # override _construct_form to add self.team to the StatisticForm upon
        # creation
        kwargs['user'] = self.instance.owned_by
        kwargs['team'] = self.instance.team
        return super(GameStatisticFormSet, self)._construct_form(index, **kwargs)


class PlayerStatisticFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(PlayerStatisticFormSet, self).__init__(*args, **kwargs)
        if 'queryset' not in kwargs:
            kwargs['queryset'] = self.instance.statistics.all()


GameStatisticModelFormSet = inlineformset_factory(
    parent_model=models.Roster, model=models.Statistic, form=GameStatisticForm,
    formset=GameStatisticFormSet, extra=15, max_num=20, fields=(
        'player', 'at_bats', 'runs', 'rbis', 'walks', 'strikeouts', 'singles',
        'doubles', 'triples', 'home_runs'
    ))


PlayerStatisticModelFormSet = inlineformset_factory(
    parent_model=models.Player, model=models.Statistic, form=StatisticForm,
    formset=PlayerStatisticFormSet, extra=0, fields=(
        'at_bats', 'runs', 'rbis', 'walks', 'strikeouts', 'singles', 'doubles',
        'triples', 'home_runs'
    ))
