from django.urls import path

from .views import CreatePlayerView

urlpatterns = [
    path('', CreatePlayerView.as_view())
]