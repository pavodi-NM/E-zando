from django.db import models

# Create your models here.
from StandardApps.models import Clients, Produits


class UserWishList(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class EnquiryMessageSujet(models.Model):
    slug = models.SlugField(unique=True)
    sujet = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.sujet)


class ClientEnquiryMessage(models.Model):
    slug = models.SlugField(unique=False)
    enquirySujet = models.ForeignKey(EnquiryMessageSujet, on_delete=models.SET_NULL, null=True, blank=True)
    sujet = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField()
    nom = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=500, null=True, blank=True)
    imageMessage = models.ImageField(upload_to='MessageEnquiry')

    def __str__(self):
        return str(self.enquirySujet)
