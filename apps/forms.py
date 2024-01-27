from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput

from apps.models import User, Emails


class RegisterForm(ModelForm):
    confirm_password = CharField(max_length=255, widget=PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirm_password')

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Confirm password is not correct')
        return make_password(password)


class EmailForm(forms.ModelForm):
    def clean_email(self):
        email = self.data.get('email')
        if Emails.objects.filter(email=email):
            raise ValidationError('Email already exists !')
        return email

    class Meta:
        model = Emails
        fields = ('email',)
