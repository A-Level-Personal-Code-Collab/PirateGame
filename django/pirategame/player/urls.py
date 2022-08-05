from django.urls import path

from .views import PlayerView

urlpatterns = [
    path('', PlayerView.as_view())
]