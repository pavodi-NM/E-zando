from django.contrib import admin

# Register your models here.
from Account.models import UserWishList, EnquiryMessageSujet, ClientEnquiryMessage


@admin.register(UserWishList)
class AdminUserWishlist(admin.ModelAdmin):
    list_display = ['id', 'client', 'produit']


@admin.register(EnquiryMessageSujet)
class AdminEnquirySujet(admin.ModelAdmin):
    list_display = ['sujet']
    prepopulated_fields = {'slug':('sujet',)}


@admin.register(ClientEnquiryMessage)
class AdminEnquiryMessage(admin.ModelAdmin):
    list_display = ['nom', 'enquirySujet']
    prepopulated_fields = {'slug':('sujet',)}
