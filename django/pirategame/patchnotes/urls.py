from django.urls import path
from .views import PatchNotesList, PatchNotesGet

urlpatterns = [
    path('', PatchNotesList.as_view()),
    path('<str:version>/', PatchNotesGet.as_view()),
]