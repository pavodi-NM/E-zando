from allauth.account.forms import SignupForm
from django import forms
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from mptt.forms import TreeNodeChoiceField

from StandardApps.models import Category, Vendeurs


class VendorRegustrationForm(forms.ModelForm):
    prenom = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'reg-fn'
    }), required=True)
    nom = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'reg-email'
    }), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'reg-phone'
    }), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',

    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',

    }))

    class Meta:
        model = Vendeurs
        fields = ['prenom', 'nom', 'email', 'phone', "password1", "password2"]


class VendorSignUpForm(SignupForm):
    adresse = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder':'Adresse'
    }), required=True)
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'reg-phone',
        'placeholder':'Telephone'
    }), required=True)
    pays = CountryField(blank_label='(Choisissez le pays)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control'
    }))

    # This init method will allow to update the fields with our own css
    def __init__(self, *args, **kwargs):
        super(VendorSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' Nom d\'utilisateur'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':'Adresse E-mail'

        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })

    def save(self, request):
        user = super(VendorSignUpForm, self).save(request)
        user.first_name = "nabil"
        vendor = Vendeurs(
            user=user,
            prenom = user,
            adresse = self.cleaned_data.get("adresse"),
            telephone=self.cleaned_data.get("phone"),
            pays=self.cleaned_data.get("pays")

        )

        vendor.save()
        return vendor.user


class VendorAddProductForm(forms.Form):
    titre = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)

    # added recently
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class':'form-control'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'row': 5
    }), required=True)

    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=True,
                                   level_indicator=mark_safe("&nbsp;&nbsp;&nbsp;"))
    prix_red_boolean = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput(attrs={
        'class':'form-check-input',
        'type':'checkbox'
    }))
    prix_red = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        "placeholder": "facultatif"
    }))

    prix_sans_red = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        "placeholder": "sans signe de dollars."
    }))

    garantie = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)

    specifications = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)

    lieu_shop = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    quantite_stock = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))
    pays = CountryField(blank_label='(Choisissez le pays)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control'
    }))


class VendorFinalForme(forms.Form):
    politique_vendeur = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)


class VendorBusinessForm(forms.Form):
    nom_business = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)

    categories_choses_vendues = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)

    adresse_shop = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    pays = CountryField(blank_label='(Choisissez le pays)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'form-control'
    }))
    """
    mode_payment_accepte = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }), required=True)
        """


class VendorLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "email",
        'class': 'form-control rounded-start'
    }), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Mot de passe",
        'class': 'form-control'
    }), required=True)


class DashtestForm(forms.Form):
    titre = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)
    slug = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }), required=True)

    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'row': 5
    }), required=True)
    image = forms.ImageField()
