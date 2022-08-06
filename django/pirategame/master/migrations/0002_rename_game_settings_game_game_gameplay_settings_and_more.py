# Generated by Django 4.0.6 on 2022-08-04 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='game_settings',
            new_name='game_gameplay_settings',
        ),
        migrations.AddField(
            model_name='player',
            name='player_is_participating',
            field=models.BooleanField(default=True),
        ),
    ]