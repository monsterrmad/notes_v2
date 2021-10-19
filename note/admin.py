from django.contrib import admin
from note.models import Note


# Note model registration for django admin
class NoteAdmin(admin.ModelAdmin):
    """
    Model admin class to display note's fields in admin page
    """
    list_display = ("id", "public", "name", "user", "date_created")


admin.site.register(Note, NoteAdmin)
