from django.urls import path
from api.views import PublicNotesListAPIView, PrivateNotesListAPIView


urlpatterns = [
    path("public", PublicNotesListAPIView.as_view()),
    path("private", PrivateNotesListAPIView.as_view())
]
