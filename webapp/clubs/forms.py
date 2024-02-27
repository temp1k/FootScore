from django import forms
from django.core.exceptions import ValidationError

from .models import *


class TeamFilterForm(forms.Form):
    name = forms.CharField(
        label='Команда',
        required=False,
        max_length=50,
        min_length=2,
    )
    country = forms.CharField(
        label='Страна',
        required=False,
    )


class TeamForm(forms.ModelForm):
    class Meta:
        model = Teams
        fields = ['full_name', 'short_name', 'city', 'image', 'coach', 'stadium', 'country']

    def clean_city(self):
        city = self.cleaned_data['city']

        if city[0].isupper():
            return city

        raise ValidationError('Город должен начинаться с заглавной буквы')


class LigaFilterForm(forms.Form):
    name = forms.CharField(
        label='Название',
        required=False,
        max_length=50,
    )
    country = forms.CharField(
        label='Страна',
        required=False,
        max_length=50,
    )


class LigaForm(forms.ModelForm):
    class Meta:
        model = Ligs
        fields = ['name', 'country']


class MatchFilter(forms.ModelForm):
    host_team = forms.CharField(
        label='Команда хозяев',
        required=False,
    )

    guest_team = forms.CharField(
        label='Команда гостей',
        required=False,
    )

    date_match = forms.DateTimeField(
        label='Дата матча',
        required=False,

    )


