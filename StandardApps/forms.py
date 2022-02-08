from django import forms
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from .models import Ordered, Clients, Vendeurs

PAYMENT_CHOICES = (
    ('carte_credit', 'Carte de credit'),
    ('paypal', 'paypal'),
    ('Mpesa', 'Mpesa'),
    ('Orange_money', 'Orange Money'),
    ('Airtel_money', 'Airtel Money')
)


class CustomerCheckoutForm(forms.Form):
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    nom = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    numero_de_telephone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    adresse = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    seconde_adresse = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    pays = CountryField(blank_label='(Choisissez le pays)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control'
    }))
    code_postal = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=False)
    entreprise = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=False)
    meme_adresse_livraison = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    mode_payment = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES, required=True)


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Ordered
        fields = ["ordered_by", "shipping_address", "mobile", "email"]


class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Nom d'utilisateur",
        'class': 'form-control rounded-start'
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Adresse e-mail",
        'class': 'form-control rounded-start'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Mot de Passe",
        'class': 'form-control rounded-start'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Confirmer Le Mot de Passe",
        'class': 'form-control rounded-start'
    }))

    class Meta:
        model = Clients
        fields = ["username", "password1", "password2", "email"]

    def clean_username(self):
        uname = self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est invalide")
        return uname

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("cet email est déjà utilisé")
        return email

    def clean_password(self):
        pass1 = self.cleaned_data.get("password1")
        pass2 = self.cleaned_data.get("password2")

        if pass1 != pass2:
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas")
        else:
            pass1 = pass2
        return pass1


class CustomerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Nom d'utilisateur",
        'class': 'form-control rounded-start'
    }), required=True)

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Mot de passe",
        'class': 'form-control rounded-start'
    }), required=True)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError("Nom d'utilisateur invalide")
        return username


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code'
    }))


class ClientReviewForm(forms.Form):
    sujet = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control'
    }), required=True)
    notes = forms.IntegerField()
