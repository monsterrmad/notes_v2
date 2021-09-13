from django.views.generic import ListView

from note.models import Note
from django.contrib.auth.models import User


class NoteHomePageView(ListView):
    model = Note
    template_name = "homepage.html"
    paginate_by = 16
    queryset = Note.objects.filter(public=True).order_by("date_edited").reverse()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Override of get_context_data
        Adds additional context params:
            total_notes to show how many notes was created by this point
            total_pub to show how many note are shared (made public)
            total_users to show how many users registered

            current template divides a view into two halves
            first half is populated by object_list_odd notes list
            second - object_list_even notes list
            ¯\_(ツ)_/¯

        :param object_list:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        # database query to count all created notes
        context["total_notes"] = Note.objects.all().count()

        # database query to count all created public notes
        context["total_pub"] = Note.objects.filter(public=True).count()

        # database query to count all registered users
        context["total_users"] = User.objects.all().count()

        # splits notes list into two halves to populate template
        context["object_list_odd"] = []
        context["object_list_even"] = []
        for i, note in enumerate(context["note_list"]):
            note.current_user_liked = note.get_user_liked(str(self.request.user))
            if i % 2 != 0:
                context["object_list_odd"].append(note)
            else:
                context["object_list_even"].append(note)
        return context
