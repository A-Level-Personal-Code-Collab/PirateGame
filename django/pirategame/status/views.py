from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StatisticSerializer
from .models import Statistic

# Create your views here.
class StatisticView(APIView):
    def get(self, request, statistic=None):
        if statistic:
            item = Statistic.objects.get(stat_name=statistic)
            serializer = StatisticSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)