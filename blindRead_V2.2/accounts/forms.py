from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts import models as acct_mdls
from django import forms
from django.db import transaction

class UserSignUpForm(UserCreationForm):

    class Meta:
        model = acct_mdls.User
        fields = ("username", "email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Inactive User', code='inactive')
