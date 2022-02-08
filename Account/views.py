from allauth.account.views import SignupView, LoginView, PasswordChangeView, PasswordResetView
from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from allauth.account.decorators import verified_email_required
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView

from Account.forms import ClientSignUpForm, CLientLoginForm, MyCustomChangePasswordForm, MyCustomResetPasswordForm
from Account.models import UserWishList
from Dashboard.forms import VendorLoginForm, VendorRegustrationForm
from StandardApps.models import Cart, BillingAddress, Vendeurs, Clients, Produits, CommandeStatus

# Account Registration
from chat.models import ClientMessages, VendeurMessages


class ClientSignUpView(SignupView):
    template_name = 'accounts/signup_client.html'

    # the previously created form class
    form_class = ClientSignUpForm
    view_name = 'signup_client'


signup_client = ClientSignUpView.as_view()


class ClientLoginView(LoginView):
    template_name = 'accounts/login_client.html'
    form_class = CLientLoginForm
    # forms = CLientLoginForm()
    view_name = 'login_client'


login_client = ClientLoginView.as_view()


class ClientChangePassword(PasswordChangeView):
    template_name = 'accounts/change-password.html'
    form_class = MyCustomChangePasswordForm
    view_name = 'change_password'


change_password = ClientChangePassword.as_view()


class ClientResetPassword(PasswordResetView):
    template_name = 'accounts/reset-password.html'
    form_class = MyCustomResetPasswordForm
    view_name = 'reset_password'


reset_password = ClientResetPassword.as_view()


class AccountOrders(View):
    def get(self, request, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                status = CommandeStatus.objects.all()
                cart = Cart.objects.filter(client=self.request.user.clients, is_ordered=True)
                context = {
                    'cart': cart,
                    'status': status
                }
                print(context)
                return render(self.request, 'account-orders.html', context)
            else:
                messages.error(self.request, "Vous n'avez aucune commande", extra_tags="danger")
                return redirect('standardApps:home')
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucune commande", extra_tags="danger")
            return redirect('standardApps:home')


def order_sorted(request, slug):
    if request.user.is_authenticated:
        status = CommandeStatus.objects.all()
        order = Cart.objects.filter(commande_status__slug=slug)
        context = {
            'order': order,
            'status': status
        }
        return render(request, "accounts/account-orders-sorted.html", context)


class AccountAdress(TemplateView):
    template_name = 'account-address.html'


class AccountPasswordRecovery(TemplateView):
    template_name = 'account-password-recovery.html'


class AccountPayment(TemplateView):
    template_name = 'account-payment.html'


class AccountProfile(TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            # cart = Cart.objects.get(client=self.request.user.clients, is_ordered=True)
            if self.request.user.is_authenticated:
                # TODO: TO Correct later because get does not return more than one, otherwise ERROR
                # bil_details = BillingAddress.objects.get(client=self.request.user.clients)
                client = Clients.objects.get(user=self.request.user)
                context = {
                    'client': client
                    # 'bil_details': bil_details
                }
                print(context)
                return render(self.request, 'account-profile.html', context)
            # else:
            # messages.error(self.request, "Vous n'avez aucune commande delivre", extra_tags="danger")
            # return redirect('standardApps:home')
        except ObjectDoesNotExist:
            messages.error(self.request, "Vous n'avez aucune commande delivree", extra_tags="danger")
            return redirect('standardApps:home')


def addtoWishlist(request, slug):
    produit = get_object_or_404(Produits, slug=slug)
    try:
        if request.user.is_authenticated:
            if UserWishList.objects.filter(client=request.user.clients, produit=produit).exists():
                wish = UserWishList.objects.get(produit=produit)
                print(wish)
                wish.delete()
                messages.info(request, "Vous avez retiré le produit de la liste de souhaits", extra_tags='danger')
            else:
                wish_prod = UserWishList.objects.create(
                    client=request.user.clients,
                    produit=produit
                )

                wish_prod.save()
                messages.info(request, "vous avez ajoute {} dans la liste de souhaits".format(slug),
                              extra_tags='success')
        else:
            messages.info(request, "Veuillez vous connecter pour ajouter a la liste de souhaits", extra_tags='danger')
        # this returns keeps the user in the same page
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    except ObjectDoesNotExist:
        messages.info(request, "Veuillez vous connecter pour ajouter a la liste de souhaits", extra_tags='danger')
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class ContactSeller(View):
    def get(self, *args, **kwargs):
        current_user = self.request.user
        client = Clients.objects.get(user=current_user)
        pk = self.kwargs['pk']
        produit = get_object_or_404(Produits, id=pk)
        seller = produit.vendeur
        messages_client = ClientMessages.objects.filter(client=client, produit=produit).order_by("id")
        messages_vendor = VendeurMessages.objects.filter(vendeur=seller, produit_vendor=produit)
        context = {
            'produit': produit,
            'seller': seller,
            'messages_client': messages_client,
            'messages_vendor': messages_vendor
        }
        if self.request.user.is_authenticated:
            return render(self.request, "contact-seller.html", context)
        else:
            url = reverse("account:login-client")
            return HttpResponseRedirect(url)

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        produit = get_object_or_404(Produits, id=pk)
        seller = produit.vendeur
        current_user = self.request.user
        current_client = Clients.objects.get(user=current_user)
        if self.request.POST.get("message"):
            message = self.request.POST.get("message")
            client = ClientMessages(
                client=current_client,
                produit=produit,
                sent_message=message
            )
            vendor = VendeurMessages(
                vendeur=seller,
                sender=current_client,
                produit_vendor=produit,
                received_message=message
            )
            vendor.save()
            client.save()
        return HttpResponseRedirect(self.request.META["HTTP_REFERER"])


class AccountWishlist(TemplateView):
    template_name = "account-wishlist.html"

    def get(self, *args, **kwargs):
        try:
            user_wishlist = UserWishList.objects.filter(client=self.request.user.clients)
            context = {
                'wishlist': user_wishlist
            }
            print(context)
            return render(self.request, 'account-wishlist.html', context)
        except UserWishList.DoesNotExist:
            messages.info(self.request, "Vous n'avez pas de liste de souhaits")
            return HttpResponseRedirect(self.request.META["HTTP_REFERER"])


def remove_from_wish_list(request, id):
    wish_list = get_object_or_404(UserWishList, id=id)
    wish_list.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


def radio_client_payment(request):
    if request.POST.get('payment'):
        type_payment = request.POST.get('payment')
        if type_payment == "vendor_contact":
            return redirect('checkout:vendor_contact_details')
        elif type_payment == "online_pay":
            return redirect('checkout:checkoutdetails')
    else:
        return redirect('account:login-client')


class AccountSingleTicket(TemplateView):
    template_name = 'account-single-ticket.html'


class AccountTickets(TemplateView):
    template_name = 'account-tickets.html'
