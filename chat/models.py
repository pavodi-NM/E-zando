from django.db import models

# Create your models here.
from StandardApps.models import User, Produits, Clients, Vendeurs


class ClientMessages(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)
    sent_message = models.CharField(max_length=500, null=True, blank=True)
    received_message = models.CharField(max_length=500, null=True, blank=True)
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("timestamp",)


class VendeurMessages(models.Model):
    vendeur = models.ForeignKey(Vendeurs, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)
    sent_message = models.CharField(max_length=500, null=True, blank=True)
    received_message = models.CharField(max_length=500, null=True, blank=True)
    produit_vendor = models.ForeignKey(Produits, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("timestamp",)


class Message(models.Model):
    sender = models.ForeignKey(Clients, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(Vendeurs, related_name="received_messages", on_delete=models.CASCADE)
    owner_message = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("timestamp",)
