from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import *

class Registration_Form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=64)
    password2 = forms.CharField(widget=forms.PasswordInput, max_length=64)

    class Meta:
        model = User
        exclude = ['last_login', 'is_admin', 'is_active', 'created_at', 'updated_at'],

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('username already taken')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise forms.ValidationError('please enter your email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email is already in use')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        password2 = cleaned_data['password2']
        if password and password2 and password2 != password:
            raise forms.ValidationError('password did not match')
        return cleaned_data

    def save(self, commit=True):
        data = self.cleaned_data

        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            phone=data['phone'],
            passwrod=data['password'],
            role=data['role'],
            dapartment=data['department']
        )

        return user

class Login_Form(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class Profile_UpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'created_at', 'updated_at']