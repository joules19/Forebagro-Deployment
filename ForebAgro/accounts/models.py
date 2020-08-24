from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.forms import ModelForm, TextInput, CharField, NumberInput, Select, PasswordInput
from django.contrib.auth import get_user_model


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "{}".format(self.username)





