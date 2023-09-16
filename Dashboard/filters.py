import django_filters
from django_filters import DateFilter, CharFilter
from StandardApps.models import *

class ProductFilter(django_filters.FilterSet):
   # start_date = DateFilter(field_name="date_cree", lookup_expr='gte')
   # end_date = DateFilter(field_name="date_cree", lookup_expr='lte')
    #nom_produit = CharFilter(field_name='titreProduit', lookup_expr='icontains')
    class Meta:
        model = Produits
        #fields = '__all__'
        fields = ['categoryProduit']