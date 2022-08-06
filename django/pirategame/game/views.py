from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle

from .serializers import GameSerializer
from status.models import Statistic

class CreateGameView(APIView):
    # Client game creation limited at 2/min to limit possibility of silliness
    throttle_classes = [ScopedRateThrottle]
    throttle_rate = "create"

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