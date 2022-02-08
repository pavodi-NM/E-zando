from django import views

from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('dashtest/', Dashtest.as_view(), name='dashtest'),
    path('dashboardAddNewProduct/', DashboardAddNewProduct.as_view(), name='dashboardAddNewProduct'),

    path('dashboardProducts/', DashboardProducts.as_view(), name='dashboardProducts'),
    path('sorted-products/<slug:slug>',sort_product, name='sorted-products'),
    path('single-product/<slug:slug>/',single_product, name='single-product'),

    path('dashboardSettings/', DashboardSettings.as_view(), name='dashboardSettings'),

    # manage products
    path('manageproduct/<int:prod_id>/', ManageProduct.as_view(), name="manageproduct"),
    path('updateproduct/<int:prod_id>/', Update_product.as_view(), name="updateproduct"),
    re_path(r'product/update/(?P<pk>\d+)/$', product_update, name="product_update"),

    path('vendorlogout/', VendorLogoutView.as_view(), name='vendorlogout'),
    path('vendorlogin/', VendorLoginPage.as_view(), name="vendorlogin"),
    path('vendor-enregistrement/', VendorEnregistrement.as_view(), name="vendor-enregistrement"),
    re_path(r'^accounts/signup/vendeur/$', signup_vendor, name = 'signup-vendeur'),


    path('dashboardSales/', DashboardSales.as_view(), name="dashboardSales"),
    path('vendor-enregistrement-business/', VendorBusiness.as_view(), name="vendor-enregistrement-business"),
    path('vendor-final-compte/', VendorFinalCompte.as_view(), name="vendor-final-compte"),
    # specify the pdf policy file in the browser
    re_path(r'^pdf', pdf, name='pdf'),


    path('dashboardPayouts/', DashboardPayouts, name='dashboardPayouts'),

    path('dashboardFavorites/', DashboardFavorites, name='dashboardFavorites'),
    path('dashboardPurchases/', DashboardPurchases, name='dashboardPurchases'),


    path('dashboadLinkToIndexPage/', DashboadLinkToIndexPage, name='dashboadLinkToIndexPage'),
    path('accountLinkToSignIn/', AccountLinkToSignIn, name='accountLinkToSignIn'),

    # signup pop up redirects
    path('sign-in-radio-vendor/', radio_vendor_signin, name="sign-in-radio-vendor"),
    #chat vendor interface
    re_path(r'account/vendor-chat/(?P<pk>\d+)/(?P<id>\d+)/$', VendorChat.as_view(), name="vendor-chat"),
    path('vendor-list-notifications/', VendorNofitications.as_view(), name="vendor-list-notifications"),

    # Chat urls
    path('chat-room-vendor/<int:pk>/<slug:slug>/', vendor_chat, name='chat-room-vendor'),
    path("ajax-vendor/<int:pk>/<slug:slug>/", ajax_load_messages_vendor, name="chatroom-ajax-vendor"),
]