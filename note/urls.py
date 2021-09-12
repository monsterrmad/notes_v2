from django.urls import path
from note.views import (NoteListView, NoteDetailView, NoteCreateView,
                        NoteUpdateView, NoteDeleteView,
                        )


urlpatterns = [
    # to a personal notes list view
    path('', NoteListView.as_view()),

    # to a note creation form
    path('create', NoteCreateView.as_view()),
    # to a note detail view (public and private)

    path('<int:pk>', NoteDetailView.as_view(), name="notes"),
    # to a note edit form

    path('<int:pk>/edit', NoteUpdateView.as_view(), name="notes_edit"),
    # to note delete form (no user input required)

    path('<int:pk>/delete', NoteDeleteView.as_view(), name="notes_delete"),
]
