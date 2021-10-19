from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
import datetime
import bleach

from api.serializers import PublicNoteSerializer, PrivateNoteSerializer, NoteEditSerializer, UserSerializer
from note.models import Note
from django.contrib.auth.models import User


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination class
    sets the page size of json response to 100
    """
    page_size = 100


class PublicNotesListAPIView(ListAPIView):
    """
    Public notes list json view class
    Does not require authentication
    Uses the public Note Serializer
    Sorts notes by the last edit date
    """
    queryset = Note.objects.filter(public=True).order_by("-date_edited")
    serializer_class = PublicNoteSerializer


class PublicNotesRetrieveAPIView(RetrieveAPIView):
    """
    Public note retrieve json view class
    Does not require authentication
    Uses the pubic Note Serializer
    Note selected by id
    """
    serializer_class = PublicNoteSerializer
    queryset = Note.objects.filter(public=True)


class PrivateNotesListAPIView(ListAPIView):
    """
    Private notes list json view class
    Requires authentication:
    by Token or Session
    Uses the private Note Serializer
    Returns only a private notes created by an authorised user
    Note selected by id
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateNoteSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Gets notes of requested user
        :return:
        """
        user = self.request.user
        return Note.objects.filter(user=user).order_by("-date_edited")


class PrivateNoteRetrieveAPIView(RetrieveAPIView):
    """
    Private note retrieve json class
    Requires authentication:
    by Token or Session
    Uses private Note Serializer
    Returns only private note created by a requested user
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateNoteSerializer

    def get_queryset(self):
        """
        Gets notes of requested user
        :return:
        """
        return Note.objects.filter(user=self.request.user)


class NoteCreateAPIView(CreateAPIView):
    """
    Private note create json class
    Requires authentication:
    by Token or Session
    Uses bleach library to sanitize html data

    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NoteEditSerializer

    def perform_create(self, serializer):
        """
        Adds author name as an author to a note user field
        Sanitizes html data in a process
        :param serializer:
        :return:
        """
        serializer.validated_data["user"] = str(self.request.user)

        # sanitizes using bleach default tags, attributes, styles
        serializer.validated_data["body"] = bleach.clean(
            serializer.validated_data["body"],
            tags=bleach.ALLOWED_TAGS,
            attributes=bleach.ALLOWED_ATTRIBUTES,
            styles=bleach.ALLOWED_STYLES,
            strip=False,
            strip_comments=False
        )

        serializer.save()


class PrivateNoteUpdateAPIView(UpdateAPIView):
    """
    Private note update json class
    Requires authentication:
    by Token or Session
    Uses stripped down Note Serializer
    Allows change to only a private note created by a requested user
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = NoteEditSerializer

    def perform_update(self, serializer):
        """
        Automatically updates date_edited field to current time
        :param serializer:
        :return:
        """
        serializer.validated_data["date_edited"] = timezone.now()
        serializer.save()

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class PrivateNoteDestroyAPIView(DestroyAPIView):
    """
    Private note destroy json class
    Requires authentication:
    by Token or Session
    Deletes only a private note created by a requested user
    """

    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)


class UserDetailAPIView(APIView):
    """
    Profile json view class
    Requires authentication:
    by Token or Session
    Uses User Serializer
    Besides information provided by the serializer
    gets some stats about user's activity
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Gets requested user object
        :return:
        """
        user = self.request.user
        return User.objects.get(username=user)

    def get_data_with_user_activity(self):
        """
        Appends activity info about the user
        :return:
        """
        user_data = self.get_user_data()

        # Generate label and data set consisting of last 6 months
        now = datetime.datetime.now()
        user_data["time_data"] = {}

        # Gets previous 6 month and amount of notes user created
        for _ in range(0, 6):
            user_data["time_data"][now.strftime("%B")] = \
                Note.objects.filter(user=self.request.user, date_created__month=now.strftime("%m")).count()

            # Gets previous month
            now = now.replace(day=1) - datetime.timedelta(days=1)

        user_data["total_notes"] = Note.objects.filter(user=self.request.user).count()
        user_data["public_notes"] = Note.objects.filter(user=self.request.user, public=True).count()
        return user_data

    def get_user_data(self):
        """
        Gets the user info from the serializer
        :return:
        """
        user_data = UserSerializer(
            self.get_queryset(),
            many=False,
            context=self.request
        ).data
        return user_data

    def get(self, request, *args, **kwargs):
        """
        GET method for the API View
        Returns response with the model and activity user data
        :return:
        """
        return Response(self.get_data_with_user_activity())


class DescriptionAPIView(TemplateView):
    """
    API description page
    """
    template_name = "api.html"
