from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from django.http.response import Http404

from note.models import Note
from note.forms import NoteEditForm


class NoteListView(ListView):
    """
    Note list view for the personal notes page
    Renders notes created by an authenticated user
    """
    model = Note
    template_name = "list_view.html"
    paginate_by = 25

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Override of get_context_data
        Adds additional context params:
            :total_notes: to show how many notes was created by an user
            :total_pub: to show how many note are shared (made public)
            :tasks: to show how many notes are not complete
            :task_completion: to calculate note completion percentage

            current template divides a view into two halves
            first half is populated by the object_list_odd notes list
            second - object_list_even notes list
            ¯\_(ツ)_/¯
        :param object_list:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        # database query to count notes created by an user
        context["total_notes"] = Note.objects.filter(user=self.user).count()

        # database query to count public notes created by an user
        context["total_pub"] = Note.objects.filter(user=self.user, public=True).count()

        # database query to count completed notes created by an user
        context["tasks"] = Note.objects.filter(user=self.user, completed=False).count()

        # tries to calculate completion percentage
        # avoids ZeroDivisionError
        try:
            context["task_completion"] = 100 - int((context["tasks"] / context["total_notes"]) * 100)
        except ZeroDivisionError:
            context["task_completion"] = 0

        # splits the notes list into two halves to populate template
        context["object_list_odd"] = []
        context["object_list_even"] = []
        for i, note in enumerate(context["note_list"]):
            if i % 2 != 0:
                context["object_list_odd"].append(note)
            else:
                context["object_list_even"].append(note)
        return context

    def get(self, request, *args, **kwargs):
        """
        Override to get method
        Sets a query set to notes only created by a current user
        Avoids unauthenticated user's ability
        to see his personal notes he doesn't have
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        # if user is authenticated set the query set
        if request.user.is_authenticated:
            self.user = request.user
            self.queryset = Note.objects.filter(user=self.user).order_by("favorite").order_by("-date_edited")
            return super(NoteListView, self).get(request, *args, **kwargs)
        # else redirect to the login page with a corresponding message
        else:
            messages.error(request, "Login to view or edit your notes")
            return redirect("/login/")


class NoteDetailView(DetailView):
    """
    Note detail view for Note model
    Only allows rendering of a note that is public
    Or current user is an author
    If note is not accessible redirects to 404 page
    """
    model = Note
    template_name = "note_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["user_liked"] = self.get_object().get_user_liked(str(self.request.user))
        return context

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.user == str(self.request.user) or obj.public:
            return obj
        else:
            raise Http404


class NoteCreateView(FormView):
    """
    Form view to create a note
    Note can be created only if an user is authenticated
    Else redirects to login page
    If form is valid a new note is saved
    and an user is redirected to a personal note list view
    """
    model = Note
    template_name = "note_edit.html"
    form_class = NoteEditForm
    success_url = "/notes"

    def get(self, *args, **kwargs):
        """
        Get Override method
        Main purpose to allow note creation only to an authenticated user
        :param args:
        :param kwargs:
        :return:
        """
        # if user is logged returns super method
        if self.request.user.is_authenticated:
            return super().get(self.request, args, kwargs)
        # else redirects to a login page with a corresponding message
        else:
            messages.error(self.request, "Login to create your notes")
            return redirect("/login/")

    def form_valid(self, form):
        """
        Form validation method
        If form is valid saves a created note
        and redirects an user to the personal note list view
        :param form:
        :return:
        """
        new_note = form.save(commit=False)
        new_note.user = self.request.user
        new_note.save()
        return redirect("/notes")


class NoteUpdateView(UpdateView):
    """
    Note update view to edit a previously created note
    Note can be edited only if current user is the author
    """
    model = Note
    template_name = "note_edit.html"
    form_class = NoteEditForm
    success_url = "/notes"

    def get_object(self, *args, **kwargs):
        """
        Get object Override method
        If user is not a note's author rises 403 permission denied
        :param args:
        :param kwargs:
        :return:
        """
        obj = super().get_object(*args, **kwargs)
        if not obj.user == str(self.request.user):
            raise PermissionDenied
        else:
            return obj

    def post(self, request, *args, **kwargs):
        """
        Post Override method
        Main purpose to allow only authenticated user to create a note
        Else redirects to login page
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # if user is authenticated returns super method
        if self.request.user:
            return super().post(self, request, *args, **kwargs)
        # else redirects to a login page with a corresponding message
        else:
            messages.error(request, "Login to create your notes")
            return redirect("/login")

    def form_valid(self, form):
        """
        Form validation Override method
        If form is valid save a newly created note
        Redirects an user to personal notes view
        :param form:
        :return:
        """
        note = form.save(commit=False)
        note.user = str(self.request.user)
        note.set_date_edited()
        note.save()
        return redirect(self.success_url)


class NoteLikeUpdateView(UpdateView):
    model = Note
    fields = ["liked_users"]

    def post(self, *args, **kwargs):
        """
        Get Override method
        Main purpose to allow note creation only to an authenticated user
        :param args:
        :param kwargs:
        :return:
        """
        # if user is logged returns super method
        if self.request.user.is_authenticated:
            note = self.get_object()
            note.change_like_user(str(self.request.user))
            note.save()
            return redirect(f"/notes/{note.pk}")
        # else redirects to a login page with a corresponding message
        else:
            messages.error(self.request, "Login to like notes")
            return redirect("/login")


class NoteDeleteView(DeleteView):
    """
    View to delete a note
    A note can be deleted only by it's author
    """
    model = Note
    success_url = "/notes"

    def get_object(self, *args, **kwargs):
        """
        Get object Override method
        Main purpose to limit user ability to delete notes
        Note can be deleted only by it's author
        Else redirects to 403 permission denied
        :param args:
        :param kwargs:
        :return:
        """
        obj = super().get_object(*args, **kwargs)
        # if current user is not the author redirects to 403 page
        if not obj.user == str(self.request.user):
            raise PermissionDenied
        else:
            return obj
