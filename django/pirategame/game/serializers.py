import random
from rest_framework.serializers import ModelSerializer

from master.models import Game

class GameSerializer(ModelSerializer):
    """Serialize game data"""

    class Meta:
        model = Game
        fields = "__all__"
        read_only_fields = ["game_id", "game_square_order"] # These fields are auto-generated when model is saved
