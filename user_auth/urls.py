from django.urls import path

from user_auth.views import RegisterView, LoginView


urlpatterns = [
    # registration form path
    path('register/', RegisterView.as_view()),

    # login form path
    path('login/', LoginView.as_view()),

    # logout path
    path('logout/', LoginView.logout_view),
]
