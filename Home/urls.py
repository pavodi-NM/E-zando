from django.urls import path
from .views import HomeElectronicStore, HomeGroceryStore, HomeFashionstore1, HomeFashionstore2, HomeParcelStore, HomeFurniturestore, HomeMarketStore
app_name = 'home'
urlpatterns = [
    path('electonic/', HomeElectronicStore, name='electonicstore' ),
    path('grocerystore/', HomeGroceryStore, name='grocerystore'),
    path('fashionstore1/', HomeFashionstore1, name='fashionstore1'),
    path('fashionstore2/', HomeFashionstore2, name='fashionstore2'),
    path('parcelstore/', HomeParcelStore, name='parcelstore'),
    path('furniturestore/', HomeFurniturestore, name='furniturestore'),
    path('marketstore/', HomeMarketStore, name='marketstore')

]