from django.db import models

class Game(models.Model):
    """Each active game has an entry in the games table"""
    game_id = models.IntegerField(primary_key=True)

class Player(models.Model):
    """Keeps track of all of the currently online players"""
    user_id = models.IntegerField(primary_key=True)
    user_nickname = models.CharField(max_length=20)
    user_game = models.ForeignKey(Game,on_delete=models.CASCADE)
    user_is_host = models.BooleanField(default=False)
