# Generated by Django 3.1.14 on 2022-08-30 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20220830_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='title_en',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Имя на английском'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='title_jp',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='Имя на японском'),
            preserve_default=False,
        ),
    ]
