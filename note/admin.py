from django.contrib import admin
from note.models import Note


# Note model registration for django admin

class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "public", "name", "user", "date_created")


admin.site.register(Note, NoteAdmin)
