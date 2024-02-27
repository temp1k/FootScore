from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse


class Countries(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    short_name = models.CharField('Сокращенное название', max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Ligs(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    country = models.ForeignKey(Countries, on_delete=models.PROTECT, verbose_name='Страна')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('liga_page', kwargs={'liga_id': self.id})

    def get_table(self, season_id):
        season = Seasons.objects.get(id=season_id)
        table = TeamStandings.objects.filter(liga=self, season=season) \
            .order_by('-points', '-number_win', '-goal_differences')
        return table

    def get_matches(self):
        matches = Matches.objects.filter(liga=self).order_by('-date_match')
        return matches

    class Meta:
        verbose_name = 'Лига'
        verbose_name_plural = 'Лиги'


class Seasons(models.Model):
    begin_year = models.IntegerField(
        verbose_name='Начало',
        help_text='Введите год',
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )
    end_year = models.IntegerField(
        verbose_name='Конец',
        help_text='Введите год',
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )

    def __str__(self):
        return f'{self.begin_year}/{str(self.end_year)[-2:]}'

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'


class Positions(models.Model):
    short_name = models.CharField('Сокращенное название', max_length=10)
    full_name = models.CharField('Полное название', max_length=50)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'


class WorkExperiense(models.Model):
    date_start = models.DateField('Начало')
    date_end = models.DateField('Конец', default=None, null=True, blank=True)

    def __str__(self):
        return f'Начало: {self.date_start} || Конец: {self.date_end}'

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыты работы'


class Judges(models.Model):
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    secondname = models.CharField('Отчество', null=True, max_length=50, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    age = models.PositiveIntegerField(verbose_name='Возраст',
                                      validators=[MinValueValidator(18), MaxValueValidator(100)])
    work_experiense = models.ForeignKey(WorkExperiense, on_delete=models.PROTECT, verbose_name='Время работы')

    def __str__(self):
        return f'{self.surname} {self.name[0]}. {self.secondname[0] + "." if self.secondname else ""}'

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'


class Coaches(models.Model):
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    secondname = models.CharField('Отчество', null=True, max_length=50, blank=True)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='media')
    age = models.PositiveIntegerField(verbose_name='Возраст',
                                      validators=[MinValueValidator(18), MaxValueValidator(100)])
    work_experiense = models.ForeignKey(WorkExperiense, on_delete=models.PROTECT, verbose_name='Время работы')

    def __str__(self):
        return f'{self.surname} {self.name[0]}. {self.secondname[0] + "." if self.secondname else ""}'

    class Meta:
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренеры'


class Stadiums(models.Model):
    name = models.CharField('Название', max_length=50, unique=True)
    address = models.TextField('Адрес')
    capacity = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Вместимость')
    history = models.TextField('История', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Стадион'
        verbose_name_plural = 'Стадионы'


class Teams(models.Model):
    full_name = models.CharField('Название', max_length=50, unique=True)
    short_name = models.CharField('Сокращенное название', max_length=20)
    city = models.CharField('Город', max_length=50)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='media')
    coach = models.OneToOneField(Coaches, on_delete=models.PROTECT, verbose_name='Тренер')
    stadium = models.ForeignKey(Stadiums, on_delete=models.PROTECT, verbose_name='Стадион')
    country = models.ForeignKey(Countries, on_delete=models.PROTECT, verbose_name='Страна')

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('club_page_players', kwargs={'team_id': self.id})

    def get_players(self):
        return Players.objects.filter(team=self)

    def get_table(self):
        liga = Ligs.objects.filter(teamstandings__team=self).first()
        last_season = Seasons.objects.order_by('-begin_year').first()
        table = TeamStandings.objects.filter(liga=liga, season=last_season) \
            .order_by('-points', '-number_win', '-goal_differences')

        return table

    def get_matches(self):
        return Matches.objects.filter(Q(host_team=self) | Q(guest_team=self)).order_by('-date_match')

    def check_favorite(self, user):
        if user.is_anonymous:
            return False
        return FavoriteTeams.objects.filter(user=user, team=self).exists()

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class Players(models.Model):
    name = models.CharField('Имя', max_length=50)
    surname = models.CharField('Фамилия', max_length=50)
    secondname = models.CharField('Отчество', null=True, blank=True, max_length=50)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='media')
    age = models.PositiveIntegerField(verbose_name='Возраст',
                                      validators=[MinValueValidator(18), MaxValueValidator(100)])
    position = models.ForeignKey(Positions, on_delete=models.PROTECT, verbose_name='Позиция')
    team = models.ForeignKey(Teams, on_delete=models.PROTECT, verbose_name='Команда')
    country = models.ForeignKey(Countries, on_delete=models.PROTECT, verbose_name='Страна')

    def __str__(self):
        return f'{self.surname} {self.name[0]}. {self.secondname[0] + "." if self.secondname else ""}'

    def get_full_name(self):
        return f'{self.surname} {self.name} {self.secondname if self.secondname else ""}'

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'


class Matches(models.Model):
    date_match = models.DateTimeField('Дата матча')
    goals_first_team = models.IntegerField(verbose_name='Голы первой команды', validators=[MinValueValidator(0)])
    goals_second_team = models.IntegerField(verbose_name='Голы второй команды', validators=[MinValueValidator(0)])
    minutes_left = models.IntegerField(verbose_name='Минут осталось', default=90)
    minutes_add = models.IntegerField(verbose_name='Минут добавлено', default=0)
    host_team = models.ForeignKey(
        Teams, on_delete=models.PROTECT,
        verbose_name='Команда хозяев', related_name='home_matches'
    )
    guest_team = models.ForeignKey(
        Teams, on_delete=models.PROTECT,
        verbose_name='Команда гостей', related_name='guest_matches'
    )
    liga = models.ForeignKey(Ligs, on_delete=models.PROTECT, verbose_name='Лига', related_name='matches')

    def __str__(self):
        return f'Матч: {self.host_team} {self.goals_first_team} : {self.goals_second_team} {self.guest_team}'

    def getTime(self):
        self_datetime = self.date_match
        return self_datetime.strftime('%H:%M')

    def getDate(self):
        self_datetime = self.date_match
        return self_datetime.strftime('%d.%m.%y')

    class Meta:
        verbose_name = 'Матч'
        verbose_name_plural = 'Матчи'


class TeamStandings(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.PROTECT, verbose_name='Команда')
    season = models.ForeignKey(Seasons, on_delete=models.PROTECT, verbose_name='Сезон')
    points = models.IntegerField('Очки', default=0)
    number_win = models.IntegerField('Побед', default=0)
    number_loose = models.IntegerField('Поражений', default=0)
    number_draw = models.IntegerField('Ничей', default=0)
    goal_differences = models.IntegerField('Разница мячей', default=0)
    liga = models.ForeignKey(Ligs, on_delete=models.PROTECT, verbose_name='Лига')

    def __str__(self):
        return f'Очки: {self.points}'

    def get_number_matches(self):
        return self.number_win + self.number_loose + self.number_draw

    class Meta:
        verbose_name = 'Турнирная позиция'
        verbose_name_plural = 'Турнирные позиции'

        permissions = [
            ('can_change_results_team_standings', 'Возможность изменять статистические данные команды'),
        ]


class FavoriteTeams(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, verbose_name='Команда')

    def __str__(self):
        return f'Пользователь: {self.user}; Команда: {self.team}'

    class Meta:
        verbose_name = 'Избранные команды'
        verbose_name_plural = 'Избранная команда'

