
from django.urls import path
from .views import *
from . import views



app_name = 'standardApps'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop-now/', show_now, name="show-now"),


    path('category-list/<slug:category_slug>/', categoryItems, name='category-list' ),
    path('category/<int:id>/<slug:slug>', categoryProducts, name="category-products"),
    path('all-category/<int:id>/<slug:slug>', allcategoryProducts, name="all-category-products"),

    path('register/', CustomerRegistrationView.as_view(),name='customerregistration'),
    path('logout/', CustomerLogoutView.as_view(),name='customerlogout'),
    path('login/', CustomerLoginView.as_view(),name='customerlogin'),

    path('vendor-form-enregistrement/', customermodalLogin.as_view(),name='vendor-form-enregistrement'),
    path('recherche-produit/', get_product_query_set,name='recherche-produit'),
    path('search-produit/', home_search_product,name='search_produit'),

    # Compare products
    path('compare-products/<slug:slug>', compare_products.as_view(), name="compare-products"),
    # category sorted products
    path('search-single-category/<slug:slug>/', single_category_search, name="search-single-category"),


    path('myapps/', Apps, name='myApps' ),
    path('contact/', Contacts, name='contact'),
    path('about/', About, name='about'),
    path('orderTracking/', OrderTracking, name='orderTracking'),
    path('simple404/', Simple404, name='simple404'),
    # chatroom url

    path('http_request/', http_req, name='http_request'),

    # video links products
    path("video-lien", lien_video, name="video-link"),




]