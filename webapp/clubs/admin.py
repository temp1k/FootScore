from django.contrib import admin
from .models import *

admin.site.register(Countries)


@admin.register(Ligs)
class LigsAdmin(admin.ModelAdmin):
    fields = ['name', 'country']


admin.site.register(Seasons)

admin.site.register(Positions)

admin.site.register(WorkExperiense)


@admin.register(Judges)
class JudgesAdmin(admin.ModelAdmin):
    fields = ['surname', 'name', 'secondname', 'age', 'rating', 'work_experiense']


admin.site.register(Coaches)

admin.site.register(Stadiums)


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'city', 'coach', 'country')


@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'secondname', 'position', 'age', 'team', 'country')
    list_filter = ["position", "team", "country", "age"]
    search_fields = ['surname', 'name', 'secondname', 'team__short_name']


admin.site.register(Matches)


@admin.register(TeamStandings)
class TeamStandingsAdmin(admin.ModelAdmin):
    list_display = ('season', 'team', 'points', 'number_win', 'number_loose', 'number_draw', 'liga')
    list_editable = ('points', 'number_win', 'number_loose', 'number_draw')
    search_fields = ['season__name', 'team__full_name', 'liga__name']
    list_filter = ['team', 'liga', 'season']
