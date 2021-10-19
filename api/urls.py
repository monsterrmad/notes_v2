from django.urls import path
from api.views import (
                       PublicNotesListAPIView, PrivateNotesListAPIView, PrivateNoteRetrieveAPIView, NoteCreateAPIView,
                       UserDetailAPIView, DescriptionAPIView, PrivateNoteUpdateAPIView, PrivateNoteDestroyAPIView,
                       PublicNotesRetrieveAPIView
                       )


urlpatterns = [
    # to note create api view
    path("create", NoteCreateAPIView.as_view()),

    # to public list api view
    path("public", PublicNotesListAPIView.as_view()),

    # to public api retrieve view
    path("public/<int:pk>", PublicNotesRetrieveAPIView.as_view()),

    # to private api view requires authentication
    path("private", PrivateNotesListAPIView.as_view()),

    # to private retrieve api
    path("private/<int:pk>", PrivateNoteRetrieveAPIView.as_view()),

    # to private update api
    path("private/<int:pk>/edit", PrivateNoteUpdateAPIView.as_view()),

    # to private destroy api
    path("private/<int:pk>/delete", PrivateNoteDestroyAPIView.as_view()),

    # to profile api view requires authentication
    path("profile", UserDetailAPIView.as_view()),

    # to api description page
    path("", DescriptionAPIView.as_view())
]
