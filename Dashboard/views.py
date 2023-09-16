import json
import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from allauth.account.views import SignupView
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect, FileResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import pickle
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic import FormView, TemplateView

from Dashboard.forms import VendorAddProductForm, VendorLoginForm, VendorRegustrationForm, VendorBusinessForm, \
    VendorFinalForme, VendorSignUpForm
from Dashboard.models import VendeurBusiness, VendorPolitique
from StandardApps.models import Produits, Vendeurs, Category, CartProduit, Clients, SousCategory, RevueProduit
from chat.models import ClientMessages, VendeurMessages, Message
from .filters import ProductFilter


class VendorLoginPage(FormView):
    template_name = "vendor-login.html"
    form_class = VendorLoginForm
    success_url = reverse_lazy("dashboardAddNewProduct")

    def get(self, *args, **kwargs):
        form = VendorLoginForm()
        context = {
            'form': form
        }
        return render(self.request, 'vendor-login.html', context)

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        print(username)
        print(pword)
        usr = authenticate(username=username, password=pword)
        print(usr)
        if usr is not None and usr.vendeurs:
            login(self.request, usr)
        else:
            messages.error(self.request, "Le mot de passe ou le nom d'utilisateur est incorrect", extra_tags="danger")
            return render(self.request, self.template_name, {"form": self.form_class, "error":
                "Le mot de passe ou l'adresse email est Incorrect"})

        return super().form_valid(form)


class VendorEnregistrement(View):
    success_url = reverse_lazy("standardApps:home")

    def get(self, *args, **kwargs):
        form = VendorRegustrationForm()
        form2 = VendorLoginForm()
        context = {
            'form': form,
            'form2': form2
        }
        return render(self.request, 'vendor-enregistrement.html', context)

    def post(self, *args, **kwargs):
        form = VendorRegustrationForm(self.request.POST or None)
        try:
            if form.is_valid():
                prenom = form.cleaned_data.get("prenom")
                nom = form.cleaned_data.get("nom")
                username = nom + prenom
                adress_email = form.cleaned_data.get("email")
                telephone = form.cleaned_data.get("phone")
                password1 = form.cleaned_data.get("password1")
                password2 = form.cleaned_data.get("password2")
                print(password1)
                print(password2)
                if password1 != password2:
                    messages.error(self.request, "Les deux mots de passent ne correspondent pas", extra_tags="danger")
                    return redirect("vendor-enregistrement")
                else:
                    pass
                # I create a user before I create a vendor
                user = User.objects.create_user(username, adress_email, password1)
                # I request a this user I just created
                usr = get(username=username)
                print(usr)
                vendor = Vendeurs(
                    user=usr,
                    prenom=prenom,
                    nom=nom,
                    email_adresse=adress_email,
                    telephone=telephone

                )
                vendor.save()
                form.instance.user = user
                login(self.request, user)

                return redirect('vendor-enregistrement-business')
        except ObjectDoesNotExist:
            messages.error(self.request, "Erreur sur le formulaire")
            return redirect("vendor-enregistrement")


class VendorSignUpView(SignupView):
    template_name = 'vendor-dashboard/vendor-signup-form-perso-info.html'

    # the previously created form class
    form_class = VendorSignUpForm
    view_name = 'signup_vendor'


signup_vendor = VendorSignUpView.as_view()

"""
    def get(self, *args, **kwargs):
        form = VendorBusinessForm()
       # all_parents = Category.objects.get(pk=0)
       # products = Produits.objects.filter(categoryProduit=all_parents)
        #level 1 gets all children, level 0 gets all parents
        their_children = Category.objects.filter(level=1)
        leaf = get(pk=1).get_leafnodes()
        descedants = get(pk=1).get_descendants()

        context = {
            'form':form,
          #  'parents':all_parents,
            'children': their_children,
            'leaf':leaf,
         #   'produits1':products,
            'descedants':descedants

        }
        return render(self.request, 'vendor-multiple-steps-register-form.html', context)
"""


class VendorBusiness(View):
    def get(self, *args, **kwargs):
        form = VendorBusinessForm()

        context = {
            'form': form,

        }
        return render(self.request, 'vendor-enregistrement-business.html', context)

    def post(self, *args, **kwargs):
        # TODO: form is not working. work on that
        form = VendorBusinessForm(self.request.POST or None)
        if form.is_valid():
            current_user = self.request.user
            vendeur = Vendeurs.objects.get(user=current_user)
            # print(vendeur)
            nom_business = form.cleaned_data.get("nom_business")
            business_type = self.request.POST.get("business_type")
            # print(business_type)
            cat_choses = form.cleaned_data.get("categories_choses_vendues")
            print(cat_choses)

            adresse_shop = form.cleaned_data.get("adresse_shop")
            print(adresse_shop)
            pays = form.cleaned_data.get("pays")

            mode_payement = self.request.POST.get("paymentmode")

            business = VendeurBusiness(
                nom_business=nom_business,
                vendeur=vendeur,
                categorie_choses_vendues=cat_choses,
                lieu_physique_shop=adresse_shop,
                pays=pays,
                type_business=business_type,
                mode_payement_accepte=mode_payement,
            )
            vendeur.businessProfile = True
            vendeur.save()
            business.save()
            return redirect('vendor-final-compte')
        return HttpResponseRedirect(reverse("vendor-enregistrement-business"))


class VendorFinalCompte(View):
    def get(self, *args, **kwargs):
        form = VendorFinalForme()
        context = {
            'form': form,
        }
        return render(self.request, 'vendor-finaliser-compte.html', context)

    def post(self, *args, **kwargs):
        # get the current vendor
        current_user = self.request.user
        vendeur = Vendeurs.objects.get(user=current_user)

        # form = VendorFinalForme(self.request.POST or None)
        try:
            if self.request.POST.get('politique'):
                policy = self.request.POST.get('politique')
                vendor_policy = VendorPolitique(
                    vendeur=vendeur,
                    politique=policy
                )
                vendor_policy.save()
                return redirect("dashboardAddNewProduct")
        except ObjectDoesNotExist:
            messages.info(self.request, 'Erreur sur le formulaire', extra_tags="danger")
            return HttpResponseRedirect(reverse('vendor-final-compte'))


# this method opens a pdf policy document for a vendor to read the terms and conditions of the site
def pdf(request):
    try:
        return FileResponse(open('E:\HGU\site_policy.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404('Page inaccessible')


class DashboardAddNewProduct(View):
    def get(self, *args, **kwargs):
        formadd = VendorAddProductForm()
        vendor = Vendeurs.objects.get(user=self.request.user)
        today = datetime.date.today()
        d_joined = vendor.joined
        time_date = d_joined + timedelta(1)
        # add days on datetime field
        print(timedelta(10))
        # add six months from the signed up date
        six_month_add = d_joined + relativedelta(months=+3)
        print(six_month_add)

        context = {
            'formadd': formadd,
            'd_joined': six_month_add
        }
        return render(self.request, 'dashboard-add-new-product.html', context)

    def post(self, *args, **kwargs):
        form = VendorAddProductForm(self.request.POST or None, self.request.FILES)
        vendeur = Vendeurs.objects.get(user=self.request.user)
        if form.is_valid():
            prod_object = Produits()
            titre = form.cleaned_data.get("titre")
            slugify_titre = slugify(titre)
            slug = form.cleaned_data.get("slug")
            image = form.cleaned_data.get("image")
            description = form.cleaned_data.get("description")
            mode_payement = self.request.POST.get("paymentmode")
            specs = form.cleaned_data.get("specifications")
            category = form.cleaned_data.get("category")
            prix_red = form.cleaned_data.get("prix_red")
            prix_sans_red = form.cleaned_data.get("prix_sans_red")
            garantie = form.cleaned_data.get("garantie")
            etat = self.request.POST.get('etat')
            lieu = form.cleaned_data.get('lieu_shop')
            quantite_stock = form.cleaned_data.get("quantite_stock")
            pays = form.cleaned_data.get("pays")
            # get the boolean value from form
            prix_red_bool = form.cleaned_data['prix_red_boolean']
            produit = Produits(
                titreProduit=titre,
                vendeur=vendeur,
                slug=slugify_titre,
                imageProduit=image,
                DescriptionProduit=description,
                specifications=specs,
                reduction=prix_red_bool,
                payment_options=mode_payement,
                categoryProduit=category,
                prixActual=prix_sans_red,
                prixDiscount=prix_red,
                garantieProduit=garantie,
                quantite_du_stock=quantite_stock,
                stateProd=etat,
                lieu=lieu,
                pays=pays,

            )
            produit.save()

        messages.info(self.request, 'Ajout du produit avec succes', extra_tags="success")
        return redirect('dashboardAddNewProduct')


class ManageProduct(View):
    def get(self, request, *args, **kwargs):

        # print("this is manage cart section")
        prod_id = self.kwargs["prod_id"]
        action = request.GET.get("action")
        product = Produits.objects.get(id=prod_id)
        if action == "edit":
            return redirect('product_update', pk=product.id)
        elif action == "rmv":
            # product = Produits.objects.get(id=prod_id)
            product.delete()
        else:
            pass
        messages.info(self.request,
                      "vous avez supprimé le produit {} de la boutique en ligne".format(product.titreProduit),
                      extra_tags="danger")
        return redirect('dashboardProducts')


def product_update(request, pk):
    product = Produits.objects.get(id=pk)
    form = VendorAddProductForm
    context = {
        'product': product,
        'form': form
    }
    return render(request, "vendor-dashboard/vendor-edit-product.html", context)


class Update_product(View):
    def get(self, *args, **kwargs):
        id = self.kwargs["id"]
        product = Produits.objects.get(id=id)
        form = VendorAddProductForm
        context = {
            'product': product,
            'form': form
        }
        return render(self.request, "vendor-dashboard/vendor-edit-product.html", context)


def sort_product(request, slug):
    subcat = SousCategory.objects.get(slug=slug)
    product = Produits.objects.filter(sousCategory__slug=slug)
    print(subcat)
    context = {
        "product": product,
        "subcat": subcat
    }
    return render(request, "vendor-dashboard/vendor-sorted-products.html", context)


def single_product(request, slug):
    product = Produits.objects.get(slug=slug)
    reviews = RevueProduit.objects.filter(produit__slug=slug)
    context = {
        'single_product': product,
        'reviews':reviews
    }
    return render(request, "vendor-dashboard/single-product.html", context)


class Dashtest(View):
    def get(self, *args, **kwargs):
        formu = VendorAddProductForm()
        context = {
            'formu': formu
        }
        return render(self.request, 'dashboard-form-test.html', context)

    def post(self, *args, **kwargs):
        form = VendorAddProductForm(self.request.POST or None, self.request.FILES)
        if form.is_valid():
            titre = form.cleaned_data.get("titre")
            print(titre)
            slug = form.cleaned_data.get("slug")
            print(slug)
            image = form.cleaned_data.get("image")
            print(image)
            category = form.cleaned_data.get("category")
            print(category)
            prix_red = form.cleaned_data.get("prix_red")
            print(prix_red)
            prix_sans_red = form.cleaned_data.get("prix_sans_red")
            print(prix_sans_red)
        return redirect('dashtest')


# this method counts the number of uploaded products by a vendor
def prodcount(request):
    if request.user.is_authenticated:
        try:
            # vendeur = get_object_or_404(Vendeurs, user=request.user)
            vendeur = Vendeurs.objects.get(user=request.user, est_vendeur=True)
            products = Produits.objects.filter(vendeur=vendeur)
            return {
                'prodcount': products.count()
            }
        except Vendeurs.DoesNotExist:
            return {}
    return {}


# this method gets the products value uploaded


class DashboardProducts(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            vendeur = Vendeurs.objects.get(user=self.request.user)
            # products = Produits.objects.filter(vendeur=vendeur) # vendeur.products_set.all()
            products = vendeur.produits_set.all()
            myfilter = ProductFilter(self.request.GET, queryset=products)
            products = myfilter.qs

            context = {
                'products': products,
                'myfilter': myfilter
            }
            return render(self.request, 'dashboard-products.html', context)
        else:
            messages.error(self.request, "Vous n'etes pas connecte")


class DashboardSettings(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            vendeur = Vendeurs.objects.get(user=self.request.user)
            context = {
                'vendeur': vendeur
            }
            return render(self.request, 'dashboard-settings.html', context)
        else:
            messages.error(self.request, "Vous n'etes pas connecte")

    def post(self, *args, **kwargs):
        vendeur = Vendeurs.objects.get(user=self.request.user)
        vb = VendeurBusiness.objects.get(vendeur=vendeur)
        if self.request.POST.get("vendeur_prenom") or self.request.POST.get("nom") or self.request.POST.get(
                "telephone") or self.request.POST.get("business_name") or self.request.POST.get("adresse_physique"):
            prenom = self.request.POST.get("vendeur_prenom")
            nom = self.request.POST.get("nom")
            telephone = self.request.POST.get("telephone")
            business_name = self.request.POST.get("business_name")
            print(business_name)
            adresse_physique = self.request.POST.get("adresse_physique")
            print(adresse_physique)

            # I save the business name in the vendeur business table which is related to vendeur
            vb.lieu_physique_shop = adresse_physique
            vb.nom_business = business_name

            vendeur.prenom = prenom
            vendeur.nom = nom
            vendeur.telephone = telephone
            vendeur.save()
            vb.save()
            return HttpResponseRedirect(reverse("dashboardSettings"))


class DashboardSales(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            vendeur = Vendeurs.objects.get(user=self.request.user)
            products = Produits.objects.filter(vendeur=vendeur)
            total = 0
            for prod in products:
                soustotal = prod.quantite_du_stock * prod.prixActual  # 2 + 20
                total += soustotal

            context = {
                'products': products,
                'total': total
            }
            return render(self.request, 'dashboard-sales.html', context)
        else:
            messages.error(self.request, "Vous n'etes pas connecte")


class VendorLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("standardApps:home")


def radio_vendor_signin(request):
    if request.POST.get('signup'):
        type_signup = request.POST.get('signup')
        print("value of sign up", type_signup)
        if type_signup == "client_signup":
            return redirect('account:signup-client')
        elif type_signup == "vendeur_signup":
            return redirect('signup-vendeur')
    elif request.POST.get('signin'):
        return redirect('account:login-client')


class VendorNofitications(View):
    def get(self, *args, **kwargs):
        current_user = self.request.user
        seller = Vendeurs.objects.get(user=current_user)

        print(seller)

        # val =  list(set(VendeurMessages.objects.values_list('produit__slug', flat=True)))
        vendor_msg = Message.objects.order_by('receiver__user__username').values('receiver__pk', 'produit',
                                                                                 'sender__pk', 'sender__user__username',
                                                                                 'produit__slug',
                                                                                 'produit__imageProduit',
                                                                                 'produit__titreProduit').distinct()
        print(vendor_msg[0])
        list_prod = []
        for v in vendor_msg[0].values():
            list_prod.append(v)

        print(list_prod[4])
        slug = list_prod[4]
        porduit_db = Produits.objects.get(slug=slug)
        message_unseen = Message.objects.filter(seen=False)
        msg_unseen_count = message_unseen.count
        context = {
            'produits': vendor_msg,
            'produit_db': porduit_db,
            'msg_unseen_count': msg_unseen_count
        }
        return render(self.request, 'vendor-dashboard/notifications-list.html', context)


class VendorChat(View):
    def get(self, *args, **kwargs):
        current_user = self.request.user

        pk = self.kwargs['pk']
        id = self.kwargs['id']
        client = get_object_or_404(Clients, id=id)
        produit = get_object_or_404(Produits, id=pk)
        seller = produit.vendeur
        messages_client = ClientMessages.objects.filter(client=client, produit=produit).order_by("id")
        messages_vendor = VendeurMessages.objects.filter(vendeur=seller, produit_vendor=produit).order_by("id")
        context = {
            'produit': produit,
            'seller': seller,
            'messages_client': messages_client,
            'messages_vendor': messages_vendor
        }
        if self.request.user.is_authenticated:
            return render(self.request, "vendor-dashboard/vendor-chat-room.html", context)
        else:
            url = reverse("account:login-client")
            return HttpResponseRedirect(url)

    def post(self, *args, **kwargs):
        pk = self.kwargs['pk']
        id = self.kwargs['id']
        client = get_object_or_404(Clients, id=id)
        produit = get_object_or_404(Produits, id=pk)
        seller = produit.vendeur
        # client_response = ClientMessages.objects.get()
        current_user = self.request.user
        if self.request.POST.get("message"):
            message = self.request.POST.get("message")
            client = ClientMessages(
                client=client,
                produit=produit,
                received_message=message
            )
            vendor = VendeurMessages(
                vendeur=seller,
                produit_vendor=produit,
                sent_message=message
            )
            vendor.save()
            client.save()
        return HttpResponseRedirect(self.request.META["HTTP_REFERER"])


def vendor_chat(request, pk, slug):
    # client as the current user
    current_user = request.user
    print(current_user)
    current_client = Clients.objects.get(pk=pk)
    print(current_client)
    # get the selected product
    product_slug = Produits.objects.get(slug=slug)
    # current vendor
    messages = []
    try:
        current_vendeur = Vendeurs.objects.get(user=current_user)
        print(product_slug)
        messages = Message.objects.filter(
            Q(sender=current_client, produit=product_slug)
        )
        messages.update(seen=True)
        messages = messages | Message.objects.filter(
            Q(receiver=current_vendeur, sender=current_client, produit=product_slug))

    except Vendeurs.DoesNotExist:
        pass
    return render(request, "vendor-dashboard/vendor-chatroom.html",
                  {"other_user": current_client, "messages": messages, "product_slug": product_slug})


def ajax_load_messages_vendor(request, pk, slug):
    current_user = request.user
    # get the current product vendor
    current_vendeur = Vendeurs.objects.get(user=current_user)
    # get the product
    produit_slug = Produits.objects.get(slug=slug)

    current_client = Clients.objects.get(pk=pk)
    messages = Message.objects.filter(seen=False).filter(
        Q(receiver=current_vendeur, sender=current_client)
    )

    message_list = [{
        "sender": message.sender,
        "message": message.message,
        "sent": message.sender.user == request.user
    } for message in messages]
    messages.update(seen=True)

    if request.method == "POST":
        # current_client = Clients.objects.get(user=current_user)
        message = json.loads(request.body)
        m = Message.objects.create(receiver=current_vendeur, owner_message=current_user
                                   , sender=current_client, produit=produit_slug,
                                   message=message)
        message_list.append({
            "sender": current_vendeur.user.username,
            "message": m.message,
            "sent": True,
        })

    print(message_list)
    return JsonResponse(message_list, safe=False)


def DashboardFavorites(request):
    return render(request, 'dashboard-favorites.html')


def DashboardPayouts(request):
    return render(request, 'dashboard-payouts.html')


def DashboardPurchases(request):
    return render(request, 'dashboard-purchases.html')


def DashboadLinkToIndexPage(request):
    return render(request, 'index.html')


def AccountLinkToSignIn(request):
    return render(request, 'vendor-enregistrement.html')
