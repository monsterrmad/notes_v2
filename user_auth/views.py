from django.views.generic import FormView, UpdateView
from user_auth.forms import RegisterForm, LoginForm, ProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
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
    model = User
    template_name = "profile.html"
    form_class = ProfileUpdateForm
    success_url = "/profile"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().get(self.request, args, kwargs)
        # else redirects to a login page with a corresponding message
        else:
            messages.error(self.request, "You are not logged in")
            return redirect("/login/")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            context["user_token"] = Token.objects.get(user=self.request.user).key
        except Token.DoesNotExist:
            context["user_token"] = None
        return context

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj

    def form_valid(self, form):
        old_password = self.request.POST.get("password")
        new_password = self.request.POST.get("new_password")
        username = self.request.user
        user = User.objects.get(username=username)

        if user.check_password(old_password):
            try:
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
            logout(self.request)
            messages.error(self.request, "Wrong password")
            return redirect("/login")

    @staticmethod
    def generate_token_view(request):
        if request.user.is_authenticated:
            user = request.user
            Token.objects.create(user=user)
            return redirect("/profile")
        else:
            messages.error(request, "You are not logged in")
            return redirect("/login")
