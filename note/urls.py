from django.urls import path
from note.views import NoteListView

urlpatterns = [
    path('', NoteListView.as_view())
]
