from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, CreateView
from StandardApps.models import *

from StandardApps.forms import CheckoutForm, CouponForm
from StandardApps.forms import CustomerCheckoutForm
from StandardApps.models import Cart, BillingAddress, CartProduit
from StandardApps.views import EcomMixin

from .paypal import PayPalClient
from paypalcheckoutsdk.orders import OrdersGetRequest
import random
import string
import sys, json


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


class Checkmeout(TemplateView):
    template_name = "check-me-out.html"


class CheckoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.clients:
            pass
        else:
            return redirect('/login/?next=/checkout-details/')
        return super().dispatch(request, *args, **kwargs)

    def get(self, *args, **kwargs):
        global form
        # get the delivery adress if one exists currently now
        try:
            billing = BillingAddress.objects.get(client=self.request.user.clients)
            form = CustomerCheckoutForm(initial={
                'prenom': self.request.user.username,
                'nom':billing.nom,
                'numero_de_telephone': billing.numero_de_telephone,
                'adresse': billing.adresse,
                'seconde_adresse': billing.seconde_adresse,
                'entreprise': billing.entreprise,
                'code_postal': billing.code_postal,
                'pays': billing.pays,
            })
        except BillingAddress.DoesNotExist:
            form = CustomerCheckoutForm()
        # get the form

        if self.request.user.is_authenticated:
            # get the cart order
            cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)

            context = {
                'form': form,
                'couponform': CouponForm(),
                'cart': cart,
                'DISPLAY_COUPON_FORM': True,

            }

        else:
            return HttpResponseRedirect("customerregistration")

        return render(self.request, "checkout-details.html", context)

    # post method
    def post(self, *args, **kwargs):
        form = CustomerCheckoutForm(self.request.POST or None)
        # print(self.request.POST)
        try:
            cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
            global billing_adress
            if form.is_valid():

                prenom = form.cleaned_data.get("prenom")
                nom = form.cleaned_data.get("nom")
                numero_telephone = form.cleaned_data.get("numero_de_telephone")
                adresse = form.cleaned_data.get("adresse")
                seconde_adresse = form.cleaned_data.get("seconde_adresse")
                pays = form.cleaned_data.get("pays")
                code_postal = form.cleaned_data.get("code_postal")
                entreprise = form.cleaned_data.get("entreprise")
                # TODO: we will add functionalities for these fields later
                # meme_adresse_livraison = form.cleaned_data.get("meme_adresse_livraison")
                # save_info = form.cleaned_data.get("save_info")
                mode_payment = form.cleaned_data.get("mode_payment")

                # get the billing address if one exists, if they exist, we update that one
                try:
                    exist_billing = BillingAddress.objects.get(client=self.request.user.clients)
                    exist_billing.client = self.request.user.clients
                    exist_billing.prenom = prenom
                    exist_billing.nom = nom
                    exist_billing.numero_de_telephone = numero_telephone
                    exist_billing.adresse = adresse
                    exist_billing.seconde_adresse = seconde_adresse
                    exist_billing.pays = pays
                    exist_billing.code_postal = code_postal
                    exist_billing.entreprise = entreprise
                    exist_billing.save()
                    cart.billing_adress = exist_billing
                # we create a new billing address if none is there
                except BillingAddress.DoesNotExist:
                    billing_adress = BillingAddress(
                        client=self.request.user.clients,
                        prenom=prenom,
                        nom=nom,
                        numero_de_telephone=numero_telephone,
                        adresse=adresse,
                        seconde_adresse=seconde_adresse,
                        pays=pays,
                        code_postal=code_postal,
                        entreprise=entreprise
                    )
                    billing_adress.save()
                    cart.billing_adress = billing_adress

                cart.total = cart.get_total()
                cart.save()
                # TODO: add redirect to the selected payment method
                if mode_payment == 'paypal':
                    return redirect('checkout:paypal-checkout-payment', mode_payment='paypal')
                elif mode_payment == 'carte_credit':
                    return redirect('checkout:carte-credit-checkout-payment', mode_payment='Carte de credit')
                elif mode_payment == 'Mpesa':
                    return redirect('checkout:mpesa-checkout-payment', mode_payment='Mpesa')
                elif mode_payment == 'Orange_money':
                    return redirect('checkout:orange-checkout-payment', mode_payment='Orange Money')
                elif mode_payment == 'Airtel_money':
                    return redirect('checkout:airtel-checkout-payment', mode_payment='Airtel Money')
                else:
                    messages.warning(self.request, "Paiement echoue")
                    return redirect('checkout:checkoutdetails')
            # return redirect('checkoutdetails')
        #  return redirect('checkoutdetails')
        except ObjectDoesNotExist:
            messages.error(self.request, "Votre panier est vide")
            return redirect("checkout:checkoutdetails")


class CheckoutPayment(View):
    def get(self, *args, **kwargs):
        return render(self.request, "checkout-payment.html")


class PaypalDisplay(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
        if cart.billing_adress:
            context = {
                'cart': cart,
                'DISPLAY_COUPON_FORM': False,
            }
            return render(self.request, 'paypal-checkout-payment.html', context)
        else:
            messages.error(self.request, "Veuillez ajouter une addresse de facturation", extra_tags="danger")
            return redirect('checkout:checkoutdetails')


@login_required
def paypalPayment(request):
    PPClient = PayPalClient()

    # Here we get the total amount of the
    cart = Cart.objects.get(client=request.user.clients, is_ordered=False)

    # get the total from the cart model method
    cart_total = cart.get_total()

    # get all products
    all_product = cart.produits.all()

    # User id
    client_id = request.user.clients

    body = json.loads(request.body)
    data = body["orderID"]
    print(data)

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value
    # trx_id = response.result.purchase_unit[0].id.value
    print(total_paid)
    print(cart_total)
    print(all_product)
    # print(trx_id)
    code_ref = create_ref_code()
    print(code_ref)
    pay = Payment.objects.create(
        client=client_id,
        amount=response.result.purchase_units[0].amount.value,
    )
    payment_id = pay.pk
    pay.save()

    Cart.objects.update(code_de_reference=code_ref, total=total_paid, is_ordered=True, payment=payment_id)
    # Here we update all paid products in cart
    for item in all_product:
        cart.total = total_paid
        cart.is_ordered = True
        cart.payment = payment_id
        cart.code_de_reference = code_ref
        item.save()
    # cart.code_de_reference = create_ref_code()
    cart.save()

    # here we update all paid products from cart prod
    CartProduit.objects.update(is_ordered=True)
    for item in all_product:
        CartProduit.objects.update(is_ordered=True)
        item.save()

    return JsonResponse("Payment a ete approuve", safe=False)


def vendor_payment_details(request):
    client = request.user.clients
    try:
        cart_produit = CartProduit.objects.filter(client=client)
        print("this is the cart product", cart_produit)
        context = {
            'cart': cart_produit
        }
        return render(request, 'vendor-dashboard/vendor-payment-contact-details.html', context)
    except ObjectDoesNotExist:
        messages.info(request, "Votre panier est vide")
        return redirect("standardApps:home")


# class for cart credit payment
class CarteCreditPayment(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
        if cart.billing_adress:
            context = {
                'cart': cart,

            }
            return render(self.request, "carte-credit-checkout-payment.html", context)
        else:
            messages.info(self.request, "Veuillez ajouter une adresse de facturation", extra_tags="danger")
            return redirect('checkout:checkoutdetails')


def stripe_charge_carte_credit(request):
    cart = Cart.objects.get(client=request.user.clients, is_ordered=False)
    amount = cart.total
    print(amount)
    if request.method == 'POST':
        print('Data', request.POST)

    return redirect(reverse('checkout:checkoutComplete', args=[amount]))


class AirtelPayment(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
        context = {
            'cart': cart,

        }
        return render(self.request, "airtel-checkout-payment.html", context)


class MpesaPayment(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
        context = {
            'cart': cart,

        }
        return render(self.request, "mpesa-checkout-payment.html", context)


class OrangePayment(View):
    def get(self, *args, **kwargs):
        cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
        context = {
            'cart': cart,

        }
        return render(self.request, "orange-checkout-payment.html", context)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "Le code n'est pas valide", extra_tags="danger")
        return redirect('checkout:checkoutdetails')


# Coupon pour acheter a moindre prix
class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                cart = Cart.objects.get(client=self.request.user.clients, is_ordered=False)
                cart.coupon = get_coupon(self.request, code)
                coupon_amount = cart.coupon.amount_coupon
                total = cart.get_total() - coupon_amount
                Cart.objects.update(total=total)
                cart.save()
                messages.success(self.request, "Votre code a ete applique avec succes", extra_tags="success")
                return redirect('checkoutdetails')

            except ObjectDoesNotExist:
                messages.info(self.request, "Le code n'est pas valide", extra_tags="danger")
                return redirect('checkout:checkoutdetails')


# Paypal client

"""
class PayPalClient:
    def __init__(self):
        self.client_id = "AfAJjTbmkp4jc_x2za1Vm44HDxX3BnHwHuEw42AceArJwOw3cLissKo_UxTrHLYLBeVMVKLm2iqOZe3x"
        self.client_secret = "EBTdlVx8xR6cXZMsdKjc1RRZBhNa_yDdAdauJv9CV5HYxWg-j71I1IcRoYk-Fol7OiqSkfENeXqmIj_W"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key, value in itr:
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
                self.object_to_json(value) if not self.is_primittive(value) else \
                    value
        return result

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item) \
                                  else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)
"""

# Here we're getting the transaction details from paypal
"""
class GetOrder(PayPalClient):
  def get_order(self, order_id):
    request = OrdersGetRequest(order_id)
    #3. Call PayPal to get the transaction
    response = self.client.execute(request)
    return response

class CaptureOrder(PayPalClient):


  def capture_order(self, order_id, debug=False):

    request = OrdersCaptureRequest(order_id)

    response = self.client.execute(request)
    if debug:
      print('Status Code: ', response.status_code)
      print('Status: ', response.result.status)
      print('Order ID: ', response.result.id)
      print('Links: ')
      for link in response.result.links:
        print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
      print('Capture Ids: ')
      for purchase_unit in response.result.purchase_units:
        for capture in purchase_unit.payments.captures:
          print ('\t', capture.id)
      print ("Buyer:")
    return response

"""


class CheckoutComplete(View):
    def get(self, *args, **kwargs):
        try:
            if self.request.user.is_authenticated:
                code_ref = Cart.objects.get(client=self.request.user.clients, is_ordered=True)
                context = {
                    'code': code_ref
                }
                return render(self.request, 'checkout-complete.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'le paiement a echoue', extra_tags='danger')
            return render(self.request, 'paypal-checkout-payment.html')


def CheckoutReview(request):
    return render(request, 'checkout-review.html')


def CheckoutShipping(request):
    return render(request, 'checkout-shipping.html')


""":key



"""
