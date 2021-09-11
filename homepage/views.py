from django.views.generic import ListView

from note.models import Note
from django.contrib.auth.models import User


class NoteHomePageView(ListView):
    model = Note
    template_name = 'homepage.html'
    queryset = Note.objects.filter(public=True).order_by('date_edited').reverse()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_notes"] = Note.objects.all().count()
        context["total_pub"] = Note.objects.filter(public=True).count()
        context["total_users"] = User.objects.all().count()

        context["object_list_odd"] = []
        context["object_list_even"] = []
        for i, note in enumerate(context["note_list"]):
            if i % 2 != 0:
                context["object_list_odd"].append(note)
            else:
                context["object_list_even"].append(note)
        return context
