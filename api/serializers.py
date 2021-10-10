from rest_framework import serializers
from note.models import Note
from django.contrib.auth.models import User


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for API Note model
    """

    class Meta:
        model = Note
        fields = ["id", "user", "name", "date_created", "date_edited", "likes", "body"]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for API User model
    """
    class Meta:
        model = User
        fields = ["username", "first_name", "email", "date_joined", "is_superuser", "last_login"]

    # def create(self, validated_data):
    #     data = super().create(validated_data)
    #     return data


