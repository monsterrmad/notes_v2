from django.urls import path
from note.views import (NoteListView, NoteDetailView, NoteCreateView,
                        NoteUpdateView, NoteDeleteView,
                        )


urlpatterns = [
    path('', NoteListView.as_view()),
    path('create', NoteCreateView.as_view()),
    path('<int:pk>', NoteDetailView.as_view(), name="notes"),
    path('<int:pk>/edit', NoteUpdateView.as_view(), name="notes_edit"),
    path('<int:pk>/delete', NoteDeleteView.as_view(), name="notes_delete"),
]
