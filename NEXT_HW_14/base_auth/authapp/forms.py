from typing import Any
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password1"] != cd["password2"]:
            raise forms.ValidationError("Passwords don't match.")
        if len(cd["password2"]) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")
        return cd["password2"]

    def clean_username(self):
        cd = self.cleaned_data
        if User.objects.filter(username=cd["username"]).exists():
            raise forms.ValidationError("Username already exists.")
        if len(cd["username"]) < 8:
            raise forms.ValidationError("Username must be at least 8 characters.")
        return cd["username"]

    def save(self, commit=True) -> User:
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password1"],
        )
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
