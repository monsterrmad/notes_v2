from django.views.generic import FormView, UpdateView
from user_auth.forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from note.models import Note
from django.contrib.auth.password_validation import validate_password, ValidationError


class RegisterView(FormView):
    """
    User registration form view
    Uses a django builtin User model

    After a successful form validation
    logs a newly registered user in
    redirects to the main page
    """
    template_name = "register.html"
    form_class = RegisterForm
    success_url = "/"

    def form_valid(self, form):
        """
        Form validation Override method
        If form is valid
        Saves a newly registered user
        Uses it's parameters (username and password1) to login the user
        :param form:
        :return:
        """
        form.save()

        # logs user
        user = authenticate(
            username=self.request.POST["username"],
            password=self.request.POST["password1"]
        )
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    """
    User login form view
    Uses a django User mode

    After a successful login
    redirects user to the main page
    """
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/"

    def form_valid(self, form):
        """
        Form valid method
        :param form:
        :return:
        """
        super(LoginView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        """
        Logs an user in
        Else redirects back to the login page
        Sends a corresponding message
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        messages.error(request, "Wrong login or password")
        return redirect("/login/")

    @staticmethod
    def logout_view(request):
        """
        Log out view
        Redirects to the login page
        :param request:
        :return:
        """
        logout(request)
        return redirect("/login/")


class ProfileView(UpdateView):
    """
    Profile view
    Consists of User information, User profile edit form and different stats
    Allows to change user's first name, email and password
    Checks old password, logs out and redirects to login page if not correct
    Validates password with django password validation
    """
    model = User
    template_name = "profile.html"
    form_class = ProfileUpdateForm
    success_url = "/profile"

    def get(self, *args, **kwargs):
        """
        Redirects to login page if not authenticated
        :param args:
        :param kwargs:
        :return:
        """
        if self.request.user.is_authenticated:
            return super().get(self.request, args, kwargs)
        # else redirects to a login page with a corresponding message
        else:
            messages.error(self.request, "You are not logged in")
            return redirect("/login/")

    def get_context_data(self, **kwargs):
        """
        Gets various information about user and user's notes:
        Total notes created
        Total notes published
        User registration date
        Generates activity data for last 6 months for data chart
        Shows user api Token if available
        Otherwise shows button to generate one
        :param kwargs:
        :return:
        """
        # calls super method
        context = super().get_context_data()

        # gets total and public notes
        context["total_notes"] = Note.objects.filter(user=self.request.user).count()
        context["total_pub"] = Note.objects.filter(user=self.request.user, public=True).count()

        # gets user's registration date
        context["date_registered"] = User.objects.get(username=self.request.user).date_joined

        # Generate label and data set consisting of last 6 months
        now = datetime.datetime.now()
        context["chart_data_labels"] = []
        context["chart_data_data"] = []

        # Gets last 6 month names and note stats
        for _ in range(0, 6):
            # Appends month name
            context["chart_data_labels"].append(now.strftime("%B"))

            # Appends amount of notes created in that mounth
            context["chart_data_data"].append(
                Note.objects.filter(user=self.request.user, date_created__month=now.strftime("%m")).count()
            )

            # Gets previous month
            now = now.replace(day=1) - datetime.timedelta(days=1)

        # Reverses list (Needed for js data filling)
        context["chart_data_labels"].reverse()
        context["chart_data_data"].reverse()

        # If token is generated passes it to context data
        try:
            context["user_token"] = Token.objects.get(user=self.request.user).key
        except Token.DoesNotExist:
            context["user_token"] = None
        return context

    def get_object(self, queryset=None):
        """
        Gets User object to edit profile form
        :param queryset:
        :return:
        """
        obj = User.objects.get(username=self.request.user)
        return obj

    def form_valid(self, form):
        """
        Validates form
        Checks if an old password is correct otherwise logs out user and redirects to the login page
        with the corresponding message
        Validates new password with django password validation function
        If changes are successful redirects to profile page with the corresponding message
        Otherwise shows error messages
        Authenticates user with the new password
        :param form:
        :return:
        """
        old_password = self.request.POST.get("password")
        new_password = self.request.POST.get("new_password")
        username = self.request.user
        user = User.objects.get(username=username)

        # Checks is old password is correct
        if user.check_password(old_password):
            try:
                # Password validation
                validate_password(new_password)
                user = form.save(commit=False)
                user.set_password(new_password)
                user.save()
                user = authenticate(self.request, username=username, password=new_password)
                login(self.request, user)
                messages.info(self.request, "Success")
                return redirect("/profile")
            except ValidationError as errors:
                for error in errors:
                    messages.error(self.request, error)
                return redirect("/profile")

        else:
            # Logs out and redirects to the login page
            logout(self.request)
            messages.error(self.request, "Wrong password")
            return redirect("/login")

    @staticmethod
    def generate_token_view(request):
        """
        Generates a new user API Token if user is authenticated
        Otherwise redirects to the login page with the corresponding message
        Deletes previous Token(s) in the process
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            user = request.user
            Token.objects.filter(user=user).delete()
            Token.objects.create(user=user)
            return redirect("/profile")
        else:
            messages.error(request, "You are not logged in")
            return redirect("/login")
