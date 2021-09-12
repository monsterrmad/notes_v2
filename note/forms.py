from django import forms
from tinymce.widgets import TinyMCE

from note.models import Note


class NoteEditForm(forms.ModelForm):
    """
    Note edit form
    The form can be used both for creating and editing
    User field is not provided as it should be done automatically
    Sets html class attributes and tags
    fields:
        :name:
        :body:
        :favorite:
        :public:
        :completed:
    """
    class Meta:
        model = Note
        fields = ["name", "body", "favorite", "public", "completed"]

    name = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "label": "Title"
        }
    ))
    body = forms.CharField(widget=TinyMCE(
        attrs={
            "class": 'form-control form-control-user',
            "label": "Body"
        }
    ))
