from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import Select


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("username", "email")
        model = get_user_model()


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Username"
        self.fields["email"].label = "Email"

