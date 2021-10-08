from rest_framework import serializers
from note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for api Event model request
    """

    class Meta:
        model = Note
        fields = ["id", "user", "name", "date_created", "date_edited", "likes", "body"]
