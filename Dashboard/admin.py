from django.contrib import admin
from Dashboard.models import *
# Register your models here.

@admin.register(VendeurBusiness)
class AdminVendeurBusiness(admin.ModelAdmin):
    list_display = ['vendeur', 'type_business', 'lieu_physique_shop']

@admin.register(VendorPolitique)
class AdminVendeurPolitique(admin.ModelAdmin):
    list_display = ['vendeur', 'politique']
