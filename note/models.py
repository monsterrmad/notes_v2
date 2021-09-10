from django.db import models
from django.utils import timezone


class Note(models.Model):
    user = models.CharField(max_length=191)
    name = models.CharField(max_length=120)

    body = models.TextField()

    date_created = models.DateTimeField()
    date_edited = models.DateTimeField()
    public = models.BooleanField()
    favorite = models.BooleanField()
    views = models.IntegerField()

    def set_date_edited(self):
        self.date_edited = timezone.now()

    def inc_views(self):
        self.views += 1
