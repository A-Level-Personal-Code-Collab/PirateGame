# Generated by Django 4.0.6 on 2022-08-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0006_alter_player_player_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='player_nickname',
            field=models.CharField(default='projector', max_length=15),
        ),
    ]