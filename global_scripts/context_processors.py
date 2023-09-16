from Account.models import UserWishList
from Dashboard.models import VendeurBusiness
from StandardApps.models import Cart, Clients, Vendeurs, Category, Produits, SousCategory
from django.template import RequestContext
from django.shortcuts import render
from dateutil.relativedelta import relativedelta
import datetime


# we get all categories parent root categories
def categories(request):
    return {
        'categories': Category.objects.filter(level=0),
        'subcategories': Category.objects.filter(level=1)
    }


def subcategories(request):
    return {
        'subcategory': SousCategory.objects.all(),
    }


# Get products such as discounted prices, best sellers, new arrivals etc

def special_products(request):
    return {
        'discount_products': Produits.objects.filter(reduction=True),
        'new_arrivals': Produits.objects.all().order_by("-id")[:4],
        'lowest_price_products': Produits.objects.all().order_by("prixActual")[:4],
        'highest_price_products': Produits.objects.all().order_by("-prixActual")[:4]
    }


def sub_categories_only(request):
    return {
        'sub': Category.objects.filter(level=1)
    }


# we get all categories parent roots and their children
def categorieswithchildren(request):
    return {
        'parent_children_categories': Category.objects.all(),
    }


def carts(request):
    total = 0
    cart_total_item = 0
    try:
        if request.user.is_authenticated:
            client = request.user.clients
            try:
                cart = Cart.objects.get(client=client, is_ordered=False)
            except Cart.DoesNotExist:
                return {}
            for cart_prod in cart.produits.all():
                total += cart_prod.get_final_price()
                cart_total_item += 1

            return {
                'cart_user': cart,
                'total_cart_user': total,
                'cart_total_item': cart_total_item
            }
        return {}
    except Clients.DoesNotExist:
        return {}


def vendeur(request):
    try:
        if request.user.is_authenticated:
            current_vendor = Vendeurs.objects.get(user=request.user)
            d_joined = current_vendor.joined
            return {
                'vendeur': current_vendor,
                'three_month_period': d_joined + relativedelta(months=+3)
            }
    except Vendeurs.DoesNotExist:
        return {}
    return {}


# This double try catch, allows when a client connects, whom is not a vendor, to return an empty dict in both
# cases as a vendor or a vendorbusiness
def vendeurbusiness(request):
    try:
        if request.user.is_authenticated:
            try:
                current_vendor = Vendeurs.objects.get(user=request.user)

                business = VendeurBusiness.objects.get(vendeur=current_vendor)
                return {
                    'business': business
                }
            except Vendeurs.DoesNotExist:
                return {}
    except VendeurBusiness.DoesNotExist:
        return {}
    return {}


def totalsale(request):
    try:
        if request.user.is_authenticated:
            vendeur = Vendeurs.objects.get(user=request.user)
            products = vendeur.produits_set.all()

            total = 0
            for prod in products:
                soustotal = prod.quantite_du_stock * prod.prixActual
                total += soustotal
                return {
                    'total': total,

                }
    except Vendeurs.DoesNotExist:
        return {}
    return {}


# User wishlist total

def wish_list_total(request):
    try:
        if request.user.is_authenticated:
            user_wish_total = UserWishList.objects.filter(client=request.user.clients)
            wish_total = user_wish_total.count()
            return {
                'wish_total': wish_total
            }
    except Clients.DoesNotExist:
        return {}
    return {}


# Get user's total orders placed
def user_total_orders(request):
    try:
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(client=request.user.clients, is_ordered=True)
            except Clients.DoesNotExist:
                return {}
        else:
            return {}
        total_orders = cart.count()
        return {
            'total_orders': total_orders
        }
    except Cart.DoesNotExist:
        return {}


def anonymous_user_cart(request):
    total = 0
    cart_total_item_anonymous = 0
    try:
        device = request.COOKIES['device']
    except KeyError:
        return {}
    try:
        if request.user.is_anonymous:
            try:
                client_device = Clients.objects.get(device=device)
                cart = Cart.objects.get(client=client_device, is_ordered=False)
                for cart_prod in cart.produits.all():
                    total += cart_prod.get_final_price()
                    cart_total_item_anonymous += 1
                return {
                    'cart_user': cart,
                    'total_cart_user': total,
                    'cart_total_item': cart_total_item_anonymous
                }
            except Cart.DoesNotExist:
                return {}
        return {}
    except Clients.DoesNotExist:
        return {}
