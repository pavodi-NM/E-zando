from django import forms


class EnquiryMessageForm(forms.Form):
    sujet = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class':'form-control',
        'rows':6
    }), required=True)

    url = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control'
    }), required=False)

    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class':'form-control',
        'type':'file'
    }), required=False)
