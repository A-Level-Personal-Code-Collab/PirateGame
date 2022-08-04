from django.db import models
from master.models import Player, Game
 
# Create your models here.
class Action(models.Model):
    """A database that stores actions currently in the pipeline"""
    action_type = models.CharField(max_length=20)
    action_perpetrator = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='perpetrator')
    action_target = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, related_name='target')
    action_game = models.ForeignKey(Game, on_delete=models.CASCADE)
    action_active = models.BooleanField(default=False)
    action_target_expression = models.CharField(max_length=200, null=True)  # Used to specify what will happen to the target's money
    action_perpetrator_expression = models.CharField(max_length=200, null=True)  # Used to specify what will happen to the perpetrator's money