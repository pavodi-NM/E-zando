
from django.urls import path
from .views import *
from . import views

app_name = 'checkout'

urlpatterns = [
    path('checkoutReview/', CheckoutReview, name='checkoutReview'),
    path('checkoutComplete/', CheckoutComplete.as_view(), name='checkoutComplete'),
    path('checkoutShipping/', CheckoutShipping, name='checkoutShipping'),


    path('paypal-checkout-payment/<mode_payment>', PaypalDisplay.as_view(), name='paypal-checkout-payment'),
    path('paypal-payment/', views.paypalPayment, name='paypal-payment'),

    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),


    path('checkoutPayment/<mode_payment>/', CheckoutPayment.as_view(), name='checkoutPayment'),
    path('mpesa-checkout-payment/', MpesaPayment.as_view(), name='mpesa-checkout-payment'),
    path('airtel-checkout-payment/', AirtelPayment.as_view(), name='airtel-checkout-payment'),
    path('orange-checkout-payment/', OrangePayment.as_view(), name='orange-checkout-payment'),
    # carte de credit payment
    path('carte-credit-checkout-payment/<mode_payment>/', CarteCreditPayment.as_view(), name='carte-credit-checkout-payment'),
    path('carte-carte-credit/',stripe_charge_carte_credit, name='stripe-carte-credit'),

    path('payment/<slug>', CheckoutPayment.as_view(), name='payment'),
    path('checkout-details/', CheckoutView.as_view(), name='checkoutdetails'),

    path('vendor-payment/contact-details', vendor_payment_details, name="vendor_contact_details")




]