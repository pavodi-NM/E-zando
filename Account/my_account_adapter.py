from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from Dashboard.models import VendeurBusiness
from StandardApps.models import Clients


class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(MyAccountAdapter, self).save_user(request,user, form, commit=False)
        # Check whether the user is a customer or a vendor based on the country
        pays = form.cleaned_data.get('pays')
        print(pays)
        if pays:
            user.est_vendeur = True
        else:
            user.est_client = True

        user.save()
        return user

    def get_login_redirect_url(self, request):
        url = super(MyAccountAdapter, self).get_login_redirect_url(request)
        if self.request.user.est_client:
            url = '/'
        elif self.request.user.est_vendeur:
            # I check whether the vendor has a business profile or not
            if self.request.user.vendeurs.businessProfile:
                url = '/dashboardAddNewProduct/'
            else:
                url = '/vendor-enregistrement-business/'
        else:
            url = '/contact/'
        return url

    def get_signup_redirect_url(self, request):
        url = super(MyAccountAdapter, self).get_signup_redirect_url(request)
        if self.request.user.est_vendeur:
            url = '/vendor-enregistrement-business/'
        elif self.request.user.est_client:
            return url
        return url

    def get_email_confirmation_redirect_url(self, request):
        url = super(MyAccountAdapter, self).get_email_confirmation_redirect_url(request)
        if self.request.user.is_authenticated:
            if self.request.user.est_client:
                url = '/'
            elif self.request.user.est_vendeur:
                url = '/vendor-enregistrement-business/'
            return url
        return url
