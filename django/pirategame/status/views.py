from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import StatisticSerializer

from .models import Statistic
from master.models import Game

# Create your views here.
class StatisticView(APIView):
    def get(self, request, statistic=None):
        if statistic:  # If a specific statistic is requested
            if statistic == "current_games":
                return Response({"stat_value": self.countActiveGames()}, status=status.HTTP_200_OK)
            
            # Return single statistic from database
            try:
                item = Statistic.objects.get(stat_name=statistic)
            except Statistic.DoesNotExist as e:
                return Response({"Error": "The statistic you requested does not exist"},status=status.HTTP_400_BAD_REQUEST)
                
            serializer = StatisticSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # ----------------- #
        # Get all statistics
        responseDict = {}
        dbItems = Statistic.objects.all()
        for item in dbItems:
            responseDict[item.stat_name] = item.stat_value
        
        responseDict["current_games"] = self.countActiveGames()

        return Response(responseDict, status=status.HTTP_200_OK)

    def countActiveGames(self):
        """Return the number of games in the database"""
        return Game.objects.count()