from django.views.generic import ListView, DetailView
from note.models import Note


class NoteListView(ListView):
    model = Note
    template_name = 'list_view.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.user = request.user
            self.queryset = Note.objects.filter(user=self.user)
        return super(NoteListView, self).get(request, *args, **kwargs)
