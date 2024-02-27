from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import *


def clubs(request):
    list_clubs = Teams.objects.all()
    form_filter_teams = TeamFilterForm(request.GET)

    if form_filter_teams.is_valid():
        if form_filter_teams.cleaned_data.get('name') != '' and form_filter_teams.cleaned_data.get('name'):
            list_clubs = list_clubs.filter(Q(full_name__icontains=form_filter_teams.cleaned_data.get('name')) |
                                           Q(short_name__icontains=form_filter_teams.cleaned_data.get('name')))

        if form_filter_teams.cleaned_data.get('country') != '' and form_filter_teams.cleaned_data.get('country'):
            list_clubs = list_clubs.filter(country__name__icontains=form_filter_teams.cleaned_data.get('country'))

    context = {
        "form": form_filter_teams,
        "list_objects": list_clubs,
    }

    return render(request, 'clubs/teams.html', context)


club_menu = [
    {'title': "Игроки", 'url_name': "club_page_players"},
    {'title': "Турнирная таблица", 'url_name': "club_page_table"},
    {'title': "Матчи", 'url_name': "club_page_matches"},
]


def club(request, team_id):
    try:
        team = Teams.objects.get(id=team_id)
        route_name = request.resolver_match.url_name
        is_favorite = team.check_favorite(request.user)

        context = {
            'menu': club_menu,
            'team': team,
            'route_name': route_name,
            'is_favorite': is_favorite,
        }
        return render(request, 'clubs/team_players.html', context)

    except Teams.DoesNotExist:
        return HttpResponseNotFound('Команда не найдена')


@login_required()
def switch_favorite_team(request, team_id):
    try:
        team = Teams.objects.get(id=team_id)
        user = request.user
        print(user.id)
        if team.check_favorite(user):
            print(FavoriteTeams.objects.filter(user=user, team=team))
            FavoriteTeams.objects.filter(user=user, team=team).delete()
            print(f'Удалено {team} из избранного')
        else:
            favorite = FavoriteTeams(user=user, team=team)
            favorite.save()
            print(f'Добавлено {team} в избранной')

        return redirect(club, team_id=team_id)

    except Teams.DoesNotExist:
        return HttpResponseNotFound('Команда не найдена')


def club_table(request, team_id):
    try:
        team = Teams.objects.get(id=team_id)
        route_name = request.resolver_match.url_name
        is_favorite = team.check_favorite(request.user)

        context = {
            'menu': club_menu,
            'team': team,
            'route_name': route_name,
            'is_favorite': is_favorite,
        }
        return render(request, 'clubs/team_table.html', context)

    except Teams.DoesNotExist:
        return HttpResponseNotFound('Команда не найдена')


def club_matches(request, team_id):
    try:
        team = Teams.objects.get(id=team_id)
        route_name = request.resolver_match.url_name
        is_favorite = team.check_favorite(request.user)

        context = {
            'menu': club_menu,
            'team': team,
            'route_name': route_name,
            'is_favorite': is_favorite,
        }
        return render(request, 'clubs/team_matches.html', context)

    except Teams.DoesNotExist:
        return HttpResponseNotFound('Команда не найдена')


def add_team(request):
    if request.method == 'POST':
        form_team = TeamForm(request.POST)

        if form_team.is_valid():
            print(form_team.cleaned_data)
            form_team.save()
            messages.success(request, f'Команда {form_team.cleaned_data["full_name"]} была успешно добавлена')
            return redirect(clubs)
        else:
            messages.warning(request, 'Неверно введены данные. Проверьте поля ввода и попробуйте еще раз.')
    else:
        form_team = TeamForm()

    context = {
        'form': form_team
    }

    return render(request, 'clubs/add_team.html', context)


@login_required()
def favorite_teams(request):
    favoriteTeams = FavoriteTeams.objects.filter(user=request.user)

    context = {
        'favorites': favoriteTeams
    }

    return render(request, 'clubs/favorite_teams.html', context)


def ligs(request):
    ligs_list = Ligs.objects.all()
    form_filter_ligs = LigaFilterForm(request.GET)

    if form_filter_ligs.is_valid():
        if form_filter_ligs.cleaned_data.get('name') != '' and form_filter_ligs.cleaned_data.get('name'):
            ligs_list = ligs_list.filter(name__icontains=form_filter_ligs.cleaned_data.get('name'))

        if form_filter_ligs.cleaned_data.get('country') != '' and form_filter_ligs.cleaned_data.get('country'):
            ligs_list = ligs_list.filter(country__name__icontains=form_filter_ligs.cleaned_data.get('country'))

    context = {
        'ligs': ligs_list,
        'form': form_filter_ligs
    }

    return render(request, 'clubs/ligs.html', context)


def league(request, liga_id):
    liga = Ligs.objects.get(id=liga_id)
    if not liga:
        return HttpResponseNotFound('Лига не найдена')

    if 'id_season' in request.GET:
        id_season = request.GET['id_season']
        season = Seasons.objects.get(id=id_season)
    else:
        season = Seasons.objects.first()

    seasons = Seasons.objects.all().order_by('-begin_year')
    table = liga.get_table(season.id)

    context = {
        'liga': liga,
        'seasons': seasons,
        'selectedSeasonId': season.id,
        'table': table,
    }

    return render(request, 'clubs/liga.html', context)


@permission_required('clubs.add_ligs')
def add_liga(request):
    if request.method == "POST":
        form_liga = LigaForm(request.POST)
        if form_liga.is_valid():
            form_liga.save()
            messages.success(request, f'Лига {form_liga.cleaned_data["name"]} была успешно добавлена')
            return redirect(ligs)
        else:
            messages.warning(request, 'Неверно введены данные. Проверьте поля ввода и попробуйте еще раз.')

    else:
        form_liga = LigaForm()

    context = {
        'form': form_liga
    }

    return render(request, 'clubs/add_liga.html', context)


@permission_required('clubs.add_players')
def add_player_with_team(request, team_id):
    return redirect(reverse('admin:clubs_players_add') + f'?team={team_id}')


@permission_required('clubs.add_teamstandings')
def add_stand_with_season_and_liga(request, season_id, liga_id):
    return redirect(reverse('admin:clubs_teamstandings_add') + f'?season={season_id}&liga={liga_id}')


@permission_required('clubs.add_season')
def add_season(request):
    return redirect(reverse('admin:clubs_seasons_add'))


def matches(request):
    leagues = Ligs.objects.all()

    context = {
        'leagues': leagues
    }

    return render(request, 'clubs/matches.html', context)
