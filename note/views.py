from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import redirect
from django.contrib import messages
from django.http.response import Http404

from note.models import Note
from note.forms import NoteCreateForm


class NoteListView(ListView):
    model = Note
    template_name = 'list_view.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NoteListView, self).get_context_data(**kwargs)
        context["total_notes"] = Note.objects.filter(user=self.user).count()
        context["total_pub"] = Note.objects.filter(user=self.user, public=True).count()
        context["tasks"] = Note.objects.filter(user=self.user, competed=False).count()
        try:
            context["task_completion"] = int((context["tasks"] / context["total_notes"]) * 100) - 100
        except ZeroDivisionError:
            context["task_completion"] = 0

        context["object_list_odd"] = []
        context["object_list_even"] = []
        for i, note in enumerate(context["note_list"]):
            if i % 2 != 0:
                context["object_list_odd"].append(note)
            else:
                context["object_list_even"].append(note)
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.user = request.user
            self.queryset = Note.objects.filter(user=self.user).order_by("date_edited").reverse()
            return super(NoteListView, self).get(request, *args, **kwargs)
        else:
            messages.error(request, "Login to view or edit your notes")
            return redirect("/login/")


class NoteDetailView(DetailView):
    model = Note
    template_name = 'note_detail.html'

    def get_object(self, queryset=None):
        obj = super(NoteDetailView, self).get_object()
        if obj.user == str(self.request.user):
            return obj
        else:
            raise Http404


class NoteCreateView(FormView):
    model = Note
    template_name = 'note_create.html'
    form_class = NoteCreateForm
    success_url = '/notes'

    def post(self, request, *args, **kwargs):
        if self.request.user:
            return super(NoteCreateView, self).post(self, request, *args, **kwargs)
        else:
            messages.error(request, "Login to create your notes")
            return redirect("/login/")

    def form_valid(self, form):
        new_note = form.save(commit=False)
        new_note.user = self.request.user
        new_note.save()
        return redirect('/notes')
