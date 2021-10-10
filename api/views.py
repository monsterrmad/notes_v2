from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
import datetime

from api.serializers import NoteSerializer, UserSerializer
from note.models import Note
from django.contrib.auth.models import User


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


class UserDetailAPIView(APIView):
    """
    Profile json view class
    Requires authentication:
    by Token, Session or Login and Password
    Uses User Serializer
    Besides information provided by the serializer
    gets some stats about user's activity
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
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
