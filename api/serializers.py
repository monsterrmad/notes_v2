from rest_framework import serializers
from note.models import Note
from django.contrib.auth.models import User


class PublicNoteSerializer(serializers.ModelSerializer):
    """
    Serializer for API Note model
    """

    class Meta:
        model = Note
        fields = ["id", "user", "name", "date_created", "date_edited", "likes", "body"]


class PrivateNoteSerializer(serializers.ModelSerializer):
    """
    Serializer for API Note model
    """

    class Meta:
        model = Note
        fields = ["id", "name", "date_created", "date_edited", "public", "favorite", "completed", "body"]


class NoteEditSerializer(serializers.ModelSerializer):
    """
    Serializer for API Note model for update view
    """

    class Meta:
        model = Note
        fields = ["name", "public", "favorite", "completed", "body"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for API User model
    """

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "date_joined", "is_superuser", "last_login"]
