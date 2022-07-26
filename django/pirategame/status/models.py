from django.db import models

class Statistic(models.Model):
    """Used to track global game statistics"""
    stat_name = models.CharField(primary_key=True,max_length=31)
    stat_value = models.IntegerField()