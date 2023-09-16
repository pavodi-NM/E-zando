from allauth.account.views import SignupView, LoginView
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from django import forms
from django.contrib import messages
from django.core import validators, exceptions
from django.core.exceptions import ValidationError
from django.shortcuts import redirect
from django_countries.base import _

from StandardApps.models import Clients, User


class ClientSignUpForm(SignupForm):
    adresse = forms.CharField(max_length=50, required=True, strip=True)

    # This init method will allow to update the fields with our own css
    def __init__(self, *args, **kwargs):
        super(ClientSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' Nom d\'utilisateur'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',

        })

        self.fields['adresse'] = forms.CharField(widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adresse'
        }), required=True)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })

    def save(self, request):
        user = super(ClientSignUpForm, self).save(request)
        user.est_client = True
        user.first_name = "je suis client"
        # Create client instance
        client = Clients(
            user=user,
            adresse=self.cleaned_data.get('adresse')
        )
        client.save()
        return client.user


class CLientLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CLientLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' Nom d\'utilisateur ou Adresse email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })

    def login(self, *args, **kwargs):
        return super(CLientLoginForm, self).login(*args, **kwargs)


class MyCustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['oldpassword'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'L\'actuel Mot de passe'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nouveau Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le Mot de passe'
        })

    def save(self):
        super(MyCustomChangePasswordForm, self).save()


class MyCustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(MyCustomResetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Adresse email'
        })

    def save(self, request, **kwargs):
        email_address = super(MyCustomResetPasswordForm, self).save(request)
        return email_address

