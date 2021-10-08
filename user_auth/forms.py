from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    """
    User registration form
    Uses a django build in User model
    Has password login and email validation
    sets html class attributes and tags
    fields:
        :first_name:
        :username:
        :email:
        :password1:
        :password2:
    """

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "First Name"
        }
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "Login"
        }
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "Email"
        }
    ))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "********"
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "********"
        }
    ))


class LoginForm(forms.Form):
    """
    User login form
    Uses django build in User model
    sets html class attributes and tags
    fields:
        :username:
        :password:
    """
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "Username"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "********"
        }
    ))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "password"]

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control form-control-user",
        }
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            "class": "form-control form-control-user",
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "Old Password"
        }
    ))
    new_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "class": "form-control form-control-user",
            "placeholder": "New Password"
        }
    ))
