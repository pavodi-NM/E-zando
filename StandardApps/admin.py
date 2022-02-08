from django.contrib import admin
from django.contrib.auth import get_user_model
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin

from eCommerceBilMarket import settings
from .models import Category
from . import models
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

admin.site.register(get_user_model())


class AdminOrder(admin.ModelAdmin):
    list_display = ['client', 'is_ordered', 'payment', 'en_cours_de_livraison', 'livraison_recue', 'billing_adress',
                    'coupon',
                    'demande_de_remboursement', 'remboursement_accepte', 'remboursement_rejete']

    # helps us to create links to the related fields in the admin panel
    list_display_links = ['client', 'billing_adress', 'payment', 'coupon']

    # helps us to filter our orders
    list_filter = ['is_ordered', 'payment', 'en_cours_de_livraison', 'livraison_recue',
                   'demande_de_remboursement', 'remboursement_accepte', 'remboursement_rejete']

    search_fields = [
        'client__nom_complet',
        'code_de_reference'
    ]


"""
class AdminCategory(admin.ModelAdmin):
    list_display = ['titre','slug']
    prepopulated_fields = {'slug': ('titre',)}
"""


@admin.register(Produits)
class AdminProduit(admin.ModelAdmin):
    list_display = ['titreProduit', 'slug']
    prepopulated_fields = {'slug': ('titreProduit',)}


@admin.register(Vendeurs)
class AdminVendeurs(admin.ModelAdmin):
    list_display = ['user', 'prenom']


# category and subcategory recursive admin model through mptt package

@admin.register(RevueProduit)
class AdminRevueProduit(admin.ModelAdmin):
    list_display = ['produit', 'client', 'sujet', 'statut', 'created_at']


admin.site.register([Clients, CartProduit, Ordered, Payment, BillingAddress, Coupon])
admin.site.register(Cart, AdminOrder)


@admin.register(SousCategory)
class AdminSousCategory(admin.ModelAdmin):
    list_display = ['titre']
    prepopulated_fields = {'slug': ('titre',)}


class AdminCategory(MPTTModelAdmin):
    list_display = ['titre']
    prepopulated_fields = {'slug': ('titre',)}


@admin.register(CommandeStatus)
class AdminCommandeStatus(admin.ModelAdmin):
    list_display = ['status']
    prepopulated_fields = {'slug': ('status',)}


admin.site.register(Category, AdminCategory)
