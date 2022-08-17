from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle

from .serializers import PlayerSerializer
from master.models import Player

# ------ Custom throttling system that will only throttle POST Requests ----- #
class CustomPostOnlyThrottle(AnonRateThrottle):
    scope = 'create'
    def allow_request(self, request, view):
        if request.method == "GET":
            return True
        return super().allow_request(request, view)
class PlayerView(APIView):
    # Client game creation limited at 2/min to limit possibility of silliness
    throttle_classes = [CustomPostOnlyThrottle]

    def post(self,request):
        serializer = PlayerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, player_id=None):
        try:
            if not player_id:
                serializer = PlayerSerializer(Player.objects.all(), many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer = PlayerSerializer(Player.objects.get(player_id=player_id))
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Player.DoesNotExist:
            return Response("The game you requested does not exist", status=status.HTTP_400_BAD_REQUEST)