from django.views.generic import ListView

from note.models import Note
from django.contrib.auth.models import User


class NoteHomePageView(ListView):
    """
    Note list view for the public notes page
    Uses pagination
    Notes can be sorted by likes and creation time
    For proper pagination stores page url params for the template
    Paginated by 25
    """
    model = Note
    template_name = "homepage.html"
    paginate_by = 25

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.page_url = ""

    def get_queryset(self):
        """
        For different sorting uses url params and sets corresponding query_set
        :return:
        """
        query_set = Note.objects.filter(public=True)
        if self.request.GET.get("sort") == "date":
            query_set = query_set.order_by("date_edited").reverse()
            self.page_url = "&sort=date"
        else:
            query_set = query_set.order_by("likes").reverse()

        return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Override of get_context_data
        Adds additional context params:
            total_notes to show how many notes was created by this point
            total_pub to show how many note are shared (made public)
            total_users to show how many users registered
            page_url to store page url to paginate properly

            current template divides a view into two halves
            first half is populated by object_list_odd notes list
            second - object_list_even notes list
            ¯\_(ツ)_/¯

        :param object_list:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)

        # set page url
        context["page_url"] = self.page_url

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
