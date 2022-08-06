from django.urls import path

from .views import CreateGameView

urlpatterns = [
    path('',CreateGameView.as_view()),
]