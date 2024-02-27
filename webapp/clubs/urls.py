from django.urls import path

from . import views

urlpatterns = [
    path('teams/', views.clubs, name='clubs_page'),
    path('teams/add/', views.add_team, name='clubs_add_page'),
    path('leagues/', views.ligs, name='ligs_page'),
    path('league/<int:liga_id>', views.league, name='liga_page'),
    path('leagues/add/', views.add_liga, name='ligs_add_page'),
    path('teams/favorite/', views.favorite_teams, name='clubs_favorite'),
    path('teams/<int:team_id>', views.club, name='club_page_players'),
    path('teams/<int:team_id>/check_favorite/', views.switch_favorite_team, name='switch_favorite_team'),
    path('teams/<int:team_id>/table', views.club_table, name='club_page_table'),
    path('teams/<int:team_id>/matches', views.club_matches, name='club_page_matches'),
    path('admin/player/add/<int:team_id>/', views.add_player_with_team, name='add_player_with_team'),
    path('admin/team_standings/add/<int:season_id>/<int:liga_id>', views.add_stand_with_season_and_liga,
         name='add_stand_with_season_and_liga'),
    path('admin/seasons/add/', views.add_season, name='add_season'),
    path('matches/', views.matches, name='matches_page')
]
