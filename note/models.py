from django.db import models
from django.utils import timezone
from django.urls import reverse
from tinymce.models import HTMLField


class Note(models.Model):
    user = models.CharField(max_length=191)
    name = models.CharField(max_length=120)

    body = HTMLField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now=True, blank=True)
    date_edited = models.DateTimeField(auto_now=True, blank=True)
    public = models.BooleanField(default=False, blank=True)
    favorite = models.BooleanField(default=False, blank=True)
    views = models.IntegerField(default=0, blank=True)
    completed = models.BooleanField(default=False, blank=True)

    def get_absolute_url(self):
        return reverse('notes', kwargs={'pk': self.pk})

    def set_date_edited(self):
        self.date_edited = timezone.now()

    def get_limited_body(self):
        if len(self.body) < 1600:
            return self.body
        else:
            return f"{self.body[:1597]}..."

    def inc_views(self):
        self.views += 1
