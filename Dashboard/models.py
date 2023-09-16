from django.db import models

# Create your models here.
from django_countries.fields import CountryField

from StandardApps.models import Vendeurs


class VendeurBusiness(models.Model):
    nom_business = models.CharField(max_length=100, default="bilocost")
    vendeur = models.ForeignKey(Vendeurs, on_delete=models.CASCADE, null=True, blank=True)
    type_business = models.CharField(max_length=50, default="detaillant")
    categorie_choses_vendues = models.CharField(max_length=200, default="electroniques")
    lieu_physique_shop = models.CharField(max_length=200, default="Kinshasa")
    pays = CountryField(multiple=False, null=True, blank=True)
    mode_payement_accepte = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nom_business

class VendorPolitique(models.Model):
    vendeur = models.ForeignKey(Vendeurs, on_delete=models.CASCADE, null=True, blank=True)
    politique = models.CharField(max_length=200, default="agree")

    def __str__(self):
        return self.politique