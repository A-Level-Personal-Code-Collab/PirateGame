# Generated by Django 4.0.6 on 2022-08-04 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(max_length=20)),
                ('action_active', models.BooleanField(default=False)),
                ('action_target_expression', models.CharField(max_length=200, null=True)),
                ('action_perpetrator_expression', models.CharField(max_length=200, null=True)),
                ('action_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.game')),
                ('action_perpetrator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='perpetrator', to='master.player')),
                ('action_target', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='target', to='master.player')),
            ],
        ),
    ]
