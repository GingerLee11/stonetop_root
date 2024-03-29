from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django import forms

from .settings import DEBUG


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')

    # TODO: Write clean function to check that no identical email or username exists
    # lower the email string so that a duplicate with a capital letter can't be considered unique
    # Also, the data should be saved lowered so that it is easier to compare


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')


class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    email = forms.CharField(widget=forms.TextInput(attrs={
        "type": "email",
        "placeholder": "Enter email...",
    }))

    def save(self, use_https, *args, **kwargs):
        return super(ResetPasswordForm, self).save(use_https=True, *args, **kwargs)

