from django.urls import path
from .views import StatisticView

urlpatterns = [
    path('',StatisticView.as_view()),
    path('<str:statistic>',StatisticView.as_view())
]