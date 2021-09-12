from django.db import models
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField


class Note(models.Model):
    """
    Note model class
    Uses tinyMCE HTML model field to enable rich text editor
    fields:
        :user: author
        :name: title
        :body: html note body
        :date_created: note creation date
        :date_edited: last time the note was edited
        :public: is note was shared for everyone to see
        :favorite: is note was pinned by a user
        :completed: is note as a task was completed
        :views: how much views note gained over time
    """
    user = models.CharField(max_length=191)
    name = models.CharField(max_length=120)

    # TinyMCE field
    body = HTMLField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now=True, blank=True)
    date_edited = models.DateTimeField(auto_now=True, blank=True)
    public = models.BooleanField(default=False, blank=True)
    favorite = models.BooleanField(default=False, blank=True)
    views = models.IntegerField(default=0, blank=True)
    completed = models.BooleanField(default=False, blank=True)

    @property
    def get_absolute_url(self):
        """
        Returns url of an object instance
        :return:
        """
        return reverse("notes", kwargs={"pk": self.pk})

    def set_date_edited(self):
        """
        Sets date_edited to the current date
        Considers timezone
        :return:
        """
        self.date_edited = timezone.now()
