# Generated by Django 4.0.6 on 2022-08-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('stat_name', models.CharField(max_length=31, primary_key=True, serialize=False)),
                ('stat_value', models.IntegerField()),
            ],
        ),
    ]
