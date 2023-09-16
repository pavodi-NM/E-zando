from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import View, TemplateView
from django.shortcuts import HttpResponse, get_object_or_404
import json

from StandardApps.forms import ClientReviewForm
from StandardApps.models import Produits, Cart, CartProduit, Clients, RevueProduit
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
from StandardApps.views import EcomMixin


class ShopSingleV2(View):
    "TODO: later, I should filter product based on the categories to display in the section you may also like"

    def get(self, *args, **kwargs):
        # get the current user
        # user = self.request.user.clients

        # get the current product selected
        url_slug = self.kwargs['slug']
        product = Produits.objects.get(slug=url_slug)
        # get the review
        review = RevueProduit.objects.filter(produit=product)

        # get the related products
        similar_products = Produits.objects.filter(categoryProduit=product.categoryProduit).exclude(slug=url_slug)[:4]

        product.viewCount += 1
        product.save()
        form = ClientReviewForm()
        context = {
            'form': form,
            'product': product,
            'review': review,
            'similar_products': similar_products
        }
        return render(self.request, 'shop-single-v2.html', context)


def Addcomment(request, slug):
    # get the page url
    url = request.META.get('HTTP_REFERER')
    # get the product url id
    print(url)

    product_id = Produits.objects.get(slug=slug)
    print(product_id)

    # get the current user
    current_user = request.user
    print(current_user)
    # send a post request to the form
    form = ClientReviewForm(request.POST or None)

    if form.is_valid():
        revue = RevueProduit()

        sujet = form.cleaned_data.get('sujet')
        comment = form.cleaned_data.get('comment')
        print(sujet)
        print(comment)

        revue.produit = product_id
        revue.client = current_user.clients
        revue.sujet = sujet
        revue.comment = comment
        revue.notes = form.cleaned_data['notes']
        revue.ip = request.META.get('REMOTE_ADDR')

        # save the data
        revue.save()
        messages.info(request, "commentaire envoye avec succes, Merci", extra_tags="success")
        return redirect(url)
    return redirect(url)


# @login_required
def Addingtocart(request, slug):
    # get the page url
    # url = request.META.get('HTTP_REFERER')

    if request.user.is_authenticated:
        client = request.user.clients

    else:
        # after setting the cookie, we grab it here
        device = request.COOKIES['device']
        # then we create the client with this cookie id
        client, created = Clients.objects.get_or_create(device=device)

    produit = get_object_or_404(Produits, slug=slug)
    produit_prix = produit.prixActual
    prod_cart, created = CartProduit.objects.get_or_create(
        produit=produit,
        client=client,
        sousTotal=produit_prix,
        is_ordered=False
    )
    cart_qs = Cart.objects.filter(client=client, is_ordered=False)
    # print(cart_qs)
    if cart_qs.exists():
        cart = cart_qs[0]

        # check if the cart product is in the cart
        if cart.produits.filter(produit__slug=produit.slug).exists():
            prod_cart.quantite += 1
            prod_cart.save()
        else:
            cart.produits.add(prod_cart)


    else:
        cart = Cart.objects.create(client=client)
        cart.produits.add(prod_cart)

    messages.info(request, 'Vous avez ajoute {} dans le panier. Veuillez procéder au paiement'.format(slug),
                  extra_tags="success")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # TODO: redirect the user to the same page where they are


# Class form of item added to cart
class ItemisAddedinCart(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
        slug = self.kwargs['slug']
        prod_slug = Produits.objects.get(slug=slug)
        context = {
            'cart': prod_slug,
            'product': prod_slug
        }
        messages.info(self.request, 'Vous avez ajoute {} dans le panier. Veuillez procéder au paiement'.format(slug))
        # return HttpResponse("Item {} is added to cart".format(slug))
        return render(self.request, 'item-is-added-to-cart.html', context)


# method form of item added to class
def IteminCart(request, slug):
    cart = Cart.objects.get(client=request.user.clients, is_ordered=False)

    context = {'cart': cart}
    messages.info(request, 'Vous avez ajoute {} dans le panier'.format(slug))
    # return HttpResponse("Item {} is added to cart".format(slug))
    return render(request, 'item-is-added-to-cart.html', context)


class ShopCart(EcomMixin, View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            client = self.request.user.clients
        else:
            # after setting the cookie, we grab it here
            device = self.request.COOKIES['device']
            # then we create the client with this cookie id
            client, created = Clients.objects.get_or_create(device=device)
        try:
            cart = Cart.objects.get(client=client, is_ordered=False)
            context = {
                'cart': cart
            }
            print(cart)
            return render(self.request, "shop-cart.html", context)

        except ObjectDoesNotExist:
            messages.info(self.request, "Votre panier est vide")
            return redirect("standardApps:home")


class ManageCart(EcomMixin, View):
    def get(self, request, *args, **kwargs):

        # print("this is manage cart section")
        cartprod_id = self.kwargs["cartprod_id"]
        action = request.GET.get("action")
        # print(cartprod_id, action)
        cartpro_obj = CartProduit.objects.get(id=cartprod_id)
        if action == "inc":
            cartpro_obj.quantite += 1
            cartpro_obj.save()
        elif action == "dcr":
            cartpro_obj.quantite -= 1
            cartpro_obj.save()
            if cartpro_obj.quantite == 0:
                cartpro_obj.delete()
        elif action == "rmv":
            cartpro_obj.delete()
        else:
            pass
        return redirect('shopcart')


class EmptyCartView(View):
    def get(self, request, *args, **kwargs):

        device = self.request.COOKIES['device']
        client = self.request.user
        try:
            if self.request.user.is_authenticated and self.request.user.clients:
                cart = Cart.objects.get(client=client)
                cart.cartproduit_set.all().delete()
                cart.total = 0
                cart.save()
            else:
                try:
                    device_client = Clients.objects.get(device=device)
                except Clients.DoesNotExist:
                    return HttpResponseRedirect(self.request.META["HTTP_REFERER"])
                cart = Cart.objects.get(client=device_client)
                cartproduct = CartProduit.objects.filter(client=device_client)
                #cart.cartproduit_set.all().delete()
                cartproduct.delete()
                cart.delete()
                cart.save()

        except ObjectDoesNotExist:
            messages.info(self.request, "Panier n'existe pas", extra_tags="danger")
            return HttpResponseRedirect(self.request.META["HTTP_REFERER"])

        return redirect("shopcart")


def ShopCategories(request):
    products_based_categories = Produits.objects.filter(
        categoryProduit = 2
    )
    context = {
        'prod_cat':products_based_categories
    }
    return render(request, 'shop-categories.html',context)


def ShopGridFT(request):
    return render(request, 'shop-grid-ft.html')


def ShopGridLS(request):
    return render(request, 'shop-grid-ls.html')


def ShopListLS(request):
    return render(request, 'shop-list-ls.html')


def ShopGridRS(request):
    return render(request, 'shop-list-rs.html')


def ShopListRS(request):
    return render(request, 'shop-category-list.html')


def ShopSingleV1(request):
    return render(request, 'shop-single-v1.html')


def ShopListFT(request):
    return render(request, 'shop-grid-ft.html')
