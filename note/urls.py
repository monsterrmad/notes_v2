from django.urls import path
from note.views import NoteListView, NoteDetailView, NoteCreateView

urlpatterns = [
    path('', NoteListView.as_view()),
    path('<int:pk>', NoteDetailView.as_view(), name="notes"),
    # path('<int:pk>/edit', NoteEditView.as_view(), name="notes_edit"),
    path('create', NoteCreateView.as_view())
]
