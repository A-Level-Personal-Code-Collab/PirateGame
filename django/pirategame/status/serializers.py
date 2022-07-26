from rest_framework import serializers
from .models import Statistic

class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = ["stat_value"]