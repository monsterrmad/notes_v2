from django.urls import path
from api.views import PublicNotesListAPIView, PrivateNotesListAPIView, UserDetailAPIView, DescriptionAPIView


urlpatterns = [
    # to public api view
    path("public", PublicNotesListAPIView.as_view()),

    # to private api view requires authentication
    path("private", PrivateNotesListAPIView.as_view()),

    # to profile api view requires authentication
    path("profile", UserDetailAPIView.as_view()),

    # to api description page
    path("", DescriptionAPIView.as_view())
]
