import random
from django.db import models

class Game(models.Model):
    """Each active game has an entry in the games table"""
    game_id = models.IntegerField(primary_key=True)
    game_title = models.CharField(max_length=30)
    game_gameplay_settings = models.JSONField()
    game_square_order = models.CharField(max_length=1000)
    game_current_round = models.IntegerField(default=0)

    def save(self, **kwargs):
        # Generate ID and play order before creating game
        self.game_id = Generate.game_id()
        self.game_square_order = Generate.square_order(int(self.game_gameplay_settings["grid_height"])*int(self.game_gameplay_settings["grid_width"]))

        super().save(**kwargs)

    def __str__(self):
        return f"{self.game_id} ({self.game_title})"

class Player(models.Model):
    """Keeps track of all of the currently online players"""
    def money_default():
        return {"bank": 0, "cash": 0}

    def retals_default():
        return {"available": []}

    player_id = models.IntegerField(primary_key=True)
    player_nickname = models.CharField(max_length=15, default="projector")
    player_game = models.ForeignKey(Game,on_delete=models.CASCADE)
    player_is_host = models.BooleanField(default=False)
    player_is_participating = models.BooleanField(default=True)
    player_money = models.JSONField(default=money_default)
    player_retaliations = models.JSONField(default=retals_default)
    player_grid = models.CharField(max_length=1000, null=True)

    def save(self, **kwargs):
        # Generate primary key before saving
        self.player_id = Generate.player_id()

        super().save(**kwargs)

    def __str__(self):
        return f"{self.player_id} ({self.player_nickname})"

class Generate:
    def game_id():
        """Generate a game ID"""
        gameID = random.randint(0,99999999)
        gameID = str(gameID).zfill(8)

        # Check games database for conflicts
        while Game.objects.filter(game_id=gameID).exists():
            gameID = random.randint(0,99999999)
            gameID = str(gameID).zfill(8)
        
        return gameID

    def player_id():
        """Generate a Player ID"""
        playerID = random.randint(0,99999999)
        playerID = str(playerID).zfill(8)

        # Check player database for conflicts
        while Player.objects.filter(player_id=playerID).exists():
            playerID = random.randint(0,99999999)
            playerID = str(playerID).zfill(8)
        
        return playerID

    def square_order(gridArea):
        """Pre-Generate the order of square selection"""
        playOrder = list(map(str,range(0,gridArea)))
        random.shuffle(playOrder)
        csvString = ",".join(playOrder)
        return csvString