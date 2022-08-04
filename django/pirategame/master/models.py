from django.db import models

class Game(models.Model):
    """Each active game has an entry in the games table"""
    game_id = models.IntegerField(primary_key=True)
    game_title = models.CharField(max_length=20)
    game_settings = models.JSONField()
    game_square_order = models.CharField(max_length=1000)
    game_current_round = models.IntegerField(default=0)

class Player(models.Model):
    """Keeps track of all of the currently online players"""
    def money_default(self):
        return {"bank": 0, "cash": 0}

    def retals_default(self):
        return {"available": []}

    player_id = models.IntegerField(primary_key=True)
    player_nickname = models.CharField(max_length=20)
    player_game = models.ForeignKey(Game,on_delete=models.CASCADE)
    player_is_host = models.BooleanField(default=False)
    player_money = models.JSONField(default=money_default)
    player_retaliations = models.JSONField(default=retals_default)
    player_grid = models.CharField(max_length=1000)
