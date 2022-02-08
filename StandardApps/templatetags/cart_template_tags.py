from django import template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.views import View

from StandardApps.models import Cart, Clients

register = template.Library()

@register.filter()
def cart_produit_tag(request):
    if request.user.is_authenticated:
        client = request.user.clients
    else:
        # after setting the cookie, we grab it here
        device = request.COOKIES['device']
        # then we create the client with this cookie id
        client, created = Clients.objects.get_or_create(device=device)

    qs = Cart.objects.filter(client=client, is_ordered=False)
    if qs.exists():
        return qs[0].produits.count()
    else:
        qs = Cart.objects.filter(client=request.user.vendeurs, is_ordered=False)
        if qs.exists():
            return qs[0].produits.count()
        return 0


@register.filter()
def get(self, *args, **kwargs):
    try:
        cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
        context = {
                'object': cart
            }
        print(cart)
        return render(self.request, "index.html", context)

    except ObjectDoesNotExist:
        #messages.error(self.request,"Votre panier est vide")
        return redirect("/")
