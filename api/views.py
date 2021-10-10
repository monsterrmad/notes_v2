from rest_framework.generics import ListAPIView
from django.views.generic import TemplateView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from api.serializers import NoteSerializer
from note.models import Note


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination class
    sets page size of json response to 100
    """
    page_size = 100


class PublicNotesListAPIView(ListAPIView):
    """
    Public notes json view class
    Does not require authentication
    Uses Note Serializer
    Sorts notes by last edit date
    """
    queryset = Note.objects.filter(public=True).order_by("-date_edited")
    serializer_class = NoteSerializer


class PrivateNotesListAPIView(ListAPIView):
    """
    Private notes json view class
    Requires authentication:
    by Token, Session or Login and Password
    Uses Note Serializer
    Returns only private notes of an authorised user
    Sorts notes by last edit date
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Gets notes of requested user
        :return:
        """
        user = self.request.user
        return Note.objects.filter(user=user).order_by("-date_edited")


class DescriptionAPIView(TemplateView):
    """
    API description page
    """
    template_name = "api.html"
