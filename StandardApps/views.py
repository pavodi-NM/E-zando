from django.contrib import messages
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, EmptyResultSet
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, View, FormView, ListView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage

from decorators.my_decorators import unauthenticated_user
from .forms import CustomerRegistrationForm, CustomerLoginForm
from .models import *
import json
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.

# this method will be called first in any template the client visits first. so, when they close the tab
# there will no more be a cookie until the load the page to create a device cookie one
# that is why KeyError must be raised first to load the page, then create a cookie of device
class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        try:
            device = request.COOKIES['device']
        except KeyError:
            return super().dispatch(request, *args, **kwargs)
        try:
            client_device = Clients.objects.get(device=device)
            print(client_device)
            try:
                cart_obj = Cart.objects.get(client=client_device)
                cart_product_obj = CartProduit.objects.filter(client=client_device)
                #
                if request.user.is_authenticated and request.user.clients:
                    # when the anonymous user logs in, we update his cart and cart product
                    cart_obj.client = request.user.clients
                    cart_product_obj.client = request.user.clients
                    # then we can delete the anonymous device in the database

                    cart_obj.save()
            except Cart.DoesNotExist:
                # this catch returns the request when a an anonymous' user's cart is empty
                return super().dispatch(request, *args, **kwargs)

        except Clients.DoesNotExist:
            # if the anonymous user doesn't have a cart yet, return the request from the view
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)


def get_product_query_set(request):
    if request.method == "POST" and request.POST.get('search_here'):
        search_here = request.POST.get('search_here')

        produits = Produits.objects.filter(
            titreProduit__icontains=search_here
        )
        context = {
            'search': search_here,
            'produit_searched': produits
        }

        return render(request, "product_search_advance.html", context)
    else:
        return redirect("standardApps:simple404")


def home_search_product(request, *args, **kwargs):
    context = {}
    if request.method == 'GET':
        search = request.GET.get("search")
        if len(search) > 0:
            produits = Produits.objects.filter(
                titreProduit__icontains=search
            )
            context = {
                'produit_searched': produits
            }
            print(search)
            print(produits)
    return render(request, "product_search_advance.html", context)


class HomeView(EcomMixin, View):
    def get(self, request, *args, **kwargs):

        # get the vendor if they want to check their products in the platform
        global vendor, product_vendor
        try:
            # get all products of the current vendor visiting the online shop
            if self.request.user.is_anonymous:
                pass
            else:
                vendor = Vendeurs.objects.get(user=self.request.user)
                product_vendor = Produits.objects.filter(vendeur=vendor)
                context = {
                    'product_vendor': product_vendor
                }
                return render(request, "index.html", context)
        except Vendeurs.DoesNotExist:
            pass

        # list of products from the database

        products = Produits.objects.all().order_by("-id")
        last_item = Produits.objects.all().order_by("-id")[:1][0]
        last_other_item = Produits.objects.all().order_by("-id")[:5][2]
        last_other_item_two = Produits.objects.all().order_by("-id")[:5][3]
        # Products with discounts
        discounts_products = Produits.objects.filter(reduction=True)

        # Vendor contact list
        vendor_last_item = last_item.vendeur.pk
        vendor_pk = last_other_item.vendeur.pk

        qs_json = json.dumps(list(Produits.objects.values()), cls=DjangoJSONEncoder)
        paginator = Paginator(products, 20)

        # hard encode the page in the url
        page_num = request.GET.get('page', 1)

        try:
            page = paginator.page(page_num)
        except EmptyPage:
            return redirect("standardApps:simple404")
        context = {
            'list_product': page,
            'qs_json': qs_json,
            'last_item': last_item,
            'last_other_item': last_other_item,
            'last_other_item_two': last_other_item_two,
            'vendor_pk': vendor_pk,
            'vendor_last_item': vendor_last_item,

        }

        return render(request, "index.html", context)


def show_now(request):
    products = Produits.objects.all()
    paginator = Paginator(products, 20)

    # hard encode the page in the url
    page_num = request.GET.get('page', 1)

    # paginator object
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        return redirect("standardApps:simple404")

    context = {
        'list_product': page,
    }

    return render(request, 'shop-now-all-products.html', context)


# show products based on sorted category products
def single_category_search(request, slug):
    sous_cat = SousCategory.objects.get(slug=slug)
    products = Produits.objects.filter(sousCategory__slug=slug)
    context = {
        'list_product': products,
        'sous_cat': sous_cat,
    }
    return render(request, "single-category-product.html", context)


# showing items based on their categories
def categoryItems(request, category_slug):
    try:
        # get the main root category selected
        category = get_object_or_404(Category, slug=category_slug)
        products = Produits.objects.filter(categoryProduit=category)

        # get all descendants children of the main root category, it returns a queryset
        all_children = get_object_or_404(Category, slug=category_slug).get_descendants()
        # create a list to append elements later
        cat_list = []

        # loop through each child in the parent root
        for each_child in all_children:
            # filter only products related to each given parent root
            prod = Produits.objects.filter(categoryProduit=each_child)

            # if the parent root is not void, append all their related products in the list
            if prod:  # if the queryset returns a value, we create a list of queryset
                cat_list.append(prod)
            else:
                pass

        # let's create a list comprehension to handle the list of list of queryset created above
        list_product = [prod for cat in cat_list for prod in cat]
        # finally, we return all the lists of products of the main parent root

        # We create a paginator to pass our list
        paginator = Paginator(list_product, 1)

        # hard encode the page in the url
        page_num = request.GET.get('page', 1)
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            return redirect("standardApps:simple404")
        context = {'all_cat_products': page}
        return render(request, 'shop-all-category.html', context)
    except ObjectDoesNotExist:
        return redirect('standardApps:simple404')


# get category products from recursive categories in shop
def categoryProducts(request, id, slug):
    try:

        category = get_object_or_404(Category, slug=slug)
        products = Produits.objects.filter(categoryProduit=category)
        context = {
            'category': category,
            'produits': products,

        }
        return render(request, 'shop-category-list.html', context)
    except ObjectDoesNotExist:
        return redirect('standardApps:simple404')


def allcategoryProducts(request, id, slug):
    try:
        # get the main root category selected
        category = get_object_or_404(Category, slug=slug)
        products = Produits.objects.filter(categoryProduit=category)

        # get all descendants children of the main root category, it returns a queryset
        all_children = get_object_or_404(Category, id=id, slug=slug).get_descendants()
        # create a list to append elements later
        cat_list = []

        # loop through each child in the parent root
        for each_child in all_children:
            # filter only products related to each given parent root
            prod = Produits.objects.filter(categoryProduit=each_child)

            # if the parent root is not void, append all their related products in the list
            if prod:  # if the queryset returns a value, we create a list of queryset
                cat_list.append(prod)
            else:
                pass

        # let's create a list comprehension to handle the list of list of queryset created above
        list_product = [prod for cat in cat_list for prod in cat]
        # finally, we return all the lists of products of the main parent root
        # We create a paginator to pass our list
        paginator = Paginator(list_product, 5)

        # hard encode the page in the url
        page_num = request.GET.get('page', 1)
        try:
            page = paginator.page(page_num)
        except EmptyPage:
            return redirect("standardApps:simple404")
        context = {
            'all_cat_products': page,
            'category': category
        }
        return render(request, 'shop-all-category.html', context)
    except ObjectDoesNotExist:
        return redirect('standardApps:simple404')


class CustomerRegistrationView(CreateView):
    template_name = "customer-registration.html"
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy("standardApps:home")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        email = form.cleaned_data.get("email")
        if password1 != password2:
            return render(self.request, self.template_name, {"form": self.form_class, "error":
                "Les deux mots de passe ne correspondent pas"})
        else:
            pass
        user = User.objects.create_user(username, email, password1)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)

    # Redirect method for a user not signed in
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("standardApps:home")


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm
    success_url = reverse_lazy("standardApps:home")

    # form_valid method is a type of post method and is available in createview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and usr.clients:
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error":
                "Le mot de passe ou le nom d'utilisateur est Incorrect"})

        return super().form_valid(form)

    # Redirect method for a user not logged in
    def get_success_url(self):
        if "next" in self.request.GET:
            next_url = self.request.GET.get("next")
            return next_url
        else:
            return self.success_url


class customermodalLogin(View):
    def get(self, request):
        list_products = Produits.objects.all()[:1]
        data = serializers.serialize('json', list_products)
        s = json.dumps(data)

        return JsonResponse({'data': s}, safe=False)


class compare_products(View):
    def get(self, *args, **kwargs):
        url_slug = self.kwargs['slug']
        # get the product
        product = Produits.objects.get(slug=url_slug)

        # categoories
        category = Category.objects.filter(level=0)
        al_cat = Category.objects.all()
        print(al_cat)
        children = Category.objects.filter(slug=product.categoryProduit).get_descendants()
        print(children)
        print(category)
        # similar products
        similar_products = Produits.objects.filter(categoryProduit=product.categoryProduit).exclude(slug=url_slug)
        context = {
            'product': product,
            'similar': similar_products,
            'category': category,

        }
        return render(self.request, 'product-compare.html', context)


def lien_video(request):
    return render(request, "video_latest_products.html")


def Contacts(request):
    return render(request, 'contacts.html')


def About(request):
    return render(request, 'about.html')


def Apps(request):
    return HttpResponse('<h1>Hello</h1>')


def OrderTracking(request):
    return render(request, 'order-tracking.html')


def Simple404(request):
    return render(request, '404-simple.html')


def http_req(request):
    return render(request, 'vendor-multiple-steps-register-form.html')
