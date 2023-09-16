from django.urls import path
from .views import *

urlpatterns = [
    path('shopcart/', ShopCart.as_view(), name='shopcart'),
   # path('add-to-cart/<int:prod_id>/', Addtocart.as_view(), name='addtocart'),
    path('managecart/<int:cartprod_id>/', ManageCart.as_view(), name='managecart'),
    path("empty-cart/", EmptyCartView.as_view(), name="emptycart"),
    path("addcomment/<slug>", Addcomment, name="addcomment"),


    path('addingtocart/<slug>/', Addingtocart, name='addingtocart'),
    path('item-added-to-cart/<slug>/', ItemisAddedinCart.as_view(), name='item-added-to-cart'),

    path('shopListRS/', ShopListRS, name='shopListRS'),


    path('shopListFT/', ShopListFT, name='shopListFT'),
    path('shopListLS/', ShopListLS, name='shopListLS'),

    path('shopCategories/', ShopCategories, name='shopCategories'),
    path('shopGridLS/', ShopGridLS, name='shopGridLS'),
    path('shopGridFT/', ShopGridFT, name='shopGridFT'),
    path('shopGridRS/', ShopGridRS, name='shopGridRS'),
    path('shopSingleV1/', ShopSingleV1, name='shopSingleV1'),
    path('shopSingleV2/<slug>/', ShopSingleV2.as_view(), name='shopSingleV2'),

]