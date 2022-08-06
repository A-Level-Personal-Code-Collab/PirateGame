from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle

from .serializers import PlayerSerializer
class CreatePlayerView(APIView):
    # Client game creation limited at 2/min to limit possibility of silliness
    throttle_classes = [ScopedRateThrottle]
    throttle_rate = "create"

    def post(self,request):
        serializer = PlayerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
