
from django.urls import path, re_path
from .views import *
app_name = 'account'
urlpatterns = [
    path('accountAdress/', AccountAdress.as_view(), name='accountAddress'),
    
    path('accountOrders/', AccountOrders.as_view(), name='accountOrders'),
    path('accountOrders/sorted/<slug:slug>', order_sorted, name='account-order-sorted'),


    # Contact seller
    re_path(r'account/contact-seller/(?P<pk>\d+)/$', ContactSeller.as_view(), name="account_contact_seller"),

    
    path('accountPayment/', AccountPayment.as_view(), name='accountPayment'),
    path('accountProfile/', AccountProfile.as_view(), name='accountProfile'),
    # wishlist
    path('accountWishlist/', AccountWishlist.as_view(), name='accountWishlist'),
    path('addWishlist/ajout_au_wishlist/<slug:slug>', addtoWishlist, name='addWishlist'),
    path('remove-from-wish-list/<int:id>', remove_from_wish_list,name='remove-from-wish-list'),

    path('accountTickets/', AccountTickets.as_view(), name='accountTickets'),

    path('accountSingleTicket/', AccountSingleTicket.as_view(), name='accountSingleTicket'),
    path('accountPasswordRecovery/', AccountPasswordRecovery.as_view(), name='accountPasswordRecovery'),
    re_path(r'^accounts/signup/client/$', signup_client, name = 'signup-client'),
    re_path(r'^accounts/signin/client/$', login_client, name = 'login-client'),
    re_path(r'^accounts/motdepasse/change/$', change_password, name = 'password-change-client'),
    re_path(r'^accounts/motdepasse/renitialise/$', reset_password, name = 'password-reset-client'),
    # proceed to payment pop up
    path('payment-client-vendor/', radio_client_payment, name="payment-radio-client"),

]