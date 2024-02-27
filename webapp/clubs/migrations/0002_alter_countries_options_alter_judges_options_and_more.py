# Generated by Django 5.0.1 on 2024-01-18 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='countries',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterModelOptions(
            name='judges',
            options={'verbose_name': 'Судья', 'verbose_name_plural': 'Судьи'},
        ),
        migrations.AlterModelOptions(
            name='ligs',
            options={'verbose_name': 'Лига', 'verbose_name_plural': 'Лиги'},
        ),
        migrations.AlterModelOptions(
            name='positions',
            options={'verbose_name': 'Позиция', 'verbose_name_plural': 'Позиции'},
        ),
        migrations.AlterModelOptions(
            name='seasons',
            options={'verbose_name': 'Сезон', 'verbose_name_plural': 'Сезоны'},
        ),
        migrations.AlterModelOptions(
            name='workexperiense',
            options={'verbose_name': 'Опыт работы', 'verbose_name_plural': 'Опыты работы'},
        ),
        migrations.AlterField(
            model_name='matches',
            name='minutes_add',
            field=models.IntegerField(default=0, verbose_name='Минут добавлено'),
        ),
        migrations.AlterField(
            model_name='workexperiense',
            name='date_end',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Конец'),
        ),
    ]
