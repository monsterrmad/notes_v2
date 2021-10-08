from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from api.serializers import NoteSerializer
from note.models import Note


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100


class PublicNotesListAPIView(ListAPIView):
    queryset = Note.objects.filter(public=True).order_by("-likes")
    serializer_class = NoteSerializer


class PrivateNotesListAPIView(ListAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NoteSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(user=user)
