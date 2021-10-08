from django.urls import path

from user_auth.views import RegisterView, LoginView, ProfileView


urlpatterns = [
    # registration form path
    path("register/", RegisterView.as_view()),

    # login form path
    path("login/", LoginView.as_view()),

    # logout path
    path("logout/", LoginView.logout_view),

    # profile path
    path("profile/", ProfileView.as_view()),
    # generate token
    path("profile/generate-token", ProfileView.generate_token_view)
]
