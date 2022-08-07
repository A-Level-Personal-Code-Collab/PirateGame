from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from .serializers import GameSerializer
from status.models import Statistic
from master.models import Game

# ------ Custom throttling system that will only throttle POST Requests ----- #
class CustomPostOnlyThrottle(AnonRateThrottle):
    scope = 'create'
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)

class GameView(APIView):
    # Client game creation limited at 2/min to limit possibility of silliness
    throttle_classes = [CustomPostOnlyThrottle]

    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Increment total number of games
            stat_total_game = Statistic.objects.get(stat_name="total_games")
            stat_total_game.stat_value += 1
            Statistic.save(stat_total_game)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, game_id=None):
        try:
            if not game_id:
                serializer = GameSerializer(Game.objects.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = GameSerializer(Game.objects.get(game_id=game_id))
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response("The game you requested does not exist", status=status.HTTP_400_BAD_REQUEST)