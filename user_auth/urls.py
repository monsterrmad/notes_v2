from django.urls import path

from user_auth.views import RegisterView, LoginView


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LoginView.logout_view),
]
