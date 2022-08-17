from django.urls import path

from .views import PlayerView

urlpatterns = [
    path('', PlayerView.as_view()),
    path('<player_id>', PlayerView.as_view()),
]