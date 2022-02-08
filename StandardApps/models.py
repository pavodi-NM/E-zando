from django.db import models
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django_countries.fields import CountryField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class User(AbstractUser):
    est_client = models.BooleanField(default=False)
    est_vendeur = models.BooleanField(default=False)


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    imageCategory = models.ImageField(upload_to='categoryImage', blank=True, null=True)
    descriptionCategory = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('standardApps:category-list', args=[self.slug])

    class MPTTMeta:
        order_insertion_by = ['titre']

    def __str__(self):
        full_path = [self.titre]
        k = self.parent
        while k is not None:
            full_path.append(k.titre)
            k = k.parent
        return ' /'.join(full_path[::1])


class SousCategory(models.Model):
    titre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre


class Clients(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    nom_complet = models.CharField(max_length=200, null=True, blank=True)
    adresse = models.CharField(max_length=200, null=True, blank=True, default="Kinshasa")
    joined_on = models.DateTimeField(auto_now_add=True)
    pays = CountryField(multiple=False, null=True, blank=True)
    device = models.CharField(max_length=100, null=True, blank=True)
    est_client = models.BooleanField(default=True)

    def __str__(self):
        if self.user:
            username = self.user.username
            # username = self.adresse
        else:
            username = self.device
        return str(username)


class Vendeurs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendeurs")
    prenom = models.CharField(max_length=200, default='Ndoyi')
    nom = models.CharField(max_length=200, default='Prospere', null=True, blank=True)
    email_adresse = models.CharField(max_length=200, default='Swede')
    telephone = models.CharField(max_length=200, default='004476983672', null=True, blank=True)
    adresse = models.CharField(max_length=200, default='Kinshasa', null=True, blank=True)
    joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    pays = CountryField(multiple=False, null=True, blank=True)
    businessProfile = models.BooleanField(default=False)
    est_vendeur = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Produits(models.Model):
    titreProduit = models.CharField(max_length=100)
    vendeur = models.ForeignKey(Vendeurs, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(unique=True)
    imageProduit = models.ImageField(upload_to='produits')
    DescriptionProduit = models.TextField(null=True, blank=True)
    categoryProduit = models.ForeignKey(Category, on_delete=models.CASCADE)
    sousCategory = models.ForeignKey(SousCategory, on_delete=models.SET_NULL, blank=True, null=True)
    reduction = models.BooleanField(default=False)
    prixDiscount = models.PositiveIntegerField(null=True, blank=True)
    prixActual = models.PositiveIntegerField()
    garantieProduit = models.CharField(max_length=300, null=True, blank=True)
    specifications = models.CharField(max_length=300, null=True, blank=True)
    payment_options = models.CharField(max_length=200, default="Main a main", blank=True, null=True)
    returnPolicy = models.CharField(max_length=300, null=True, blank=True)
    viewCount = models.PositiveIntegerField(default=0)
    quantite_du_stock = models.PositiveIntegerField(default=1)
    stateProd = models.CharField(max_length=20, null=True, blank=True)
    est_en_stock = models.BooleanField(default=True)
    date_cree = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    est_actif = models.BooleanField(default=True)
    pays = CountryField(multiple=False, null=True, blank=True)
    lieu = models.CharField(max_length=200, null=True, blank=True, default="Kinshasa")
    livraison_time = models.IntegerField(default=1)

    # Lieu du produit

    def __str__(self):
        return self.titreProduit

    def get_absolute_url(self):
        return reverse('shopSingleV2', kwargs={'slug': self.slug})

    def get_adding_to_cart_url(self):
        return reverse('addingtocart', kwargs={'slug': self.slug})


class CartProduit(models.Model):  # OrderItem
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(null=True, blank=True)
    quantite = models.PositiveIntegerField(default=1)
    sousTotal = models.PositiveIntegerField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantite} of {self.produit.titreProduit}"

    def get_total_produit_price(self):
        return self.quantite * self.produit.prixActual

    def get_total_discount_produit_price(self):
        return self.quantite * self.produit.prixDiscount

    def get_amount_saved(self):
        return self.get_total_produit_price() - self.get_total_discount_produit_price()

    def get_final_price(self):
        if self.produit.prixDiscount:
            return self.get_total_discount_produit_price()
        return self.get_total_produit_price()


class RevueProduit(models.Model):
    STATUT = (
        ('Nouveau', 'Nouveau'),
        ('True', 'True'),
        ('False', 'False'),
    )

    produit = models.ForeignKey(Produits, on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, blank=True, null=True)
    sujet = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    notes = models.IntegerField(default=1)
    statut = models.CharField(max_length=10, choices=STATUT, default='Nouveau')
    ip = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sujet


class CommandeStatus(models.Model):  # Order Status
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=200, null=True, blank=True)


class Cart(models.Model):  # Order
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    produits = models.ManyToManyField(CartProduit)
    code_de_reference = models.CharField(max_length=20)
    total = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)  # Ordered Date
    is_ordered = models.BooleanField(default=False)
    billing_adress = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    commande_status = models.ForeignKey('CommandeStatus', on_delete=models.SET_NULL, blank=True, null=True)
    en_cours_de_livraison = models.BooleanField(default=False)
    livraison_recue = models.BooleanField(default=False)
    demande_de_remboursement = models.BooleanField(default=False)
    remboursement_accepte = models.BooleanField(default=False)
    remboursement_rejete = models.BooleanField(default=False)

    def __str__(self):
        if self.client.user:
            username = self.client.user.username
            # username = self.is_ordered
        else:
            username = self.client.device
        return username

    def get_total(self):
        total = 0
        for cart_item in self.produits.all():
            total += cart_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount_coupon
        return total


ORDER_ETAT = (
    ("Commande Recu", "Commande Recu"),
    ("Commande en cours de traitement", "Commande en cours de traitement"),
    ('En route', "En route"),
    ("Commande delivre", "Commande delivre"),
    ("Commande annule", "Commande annule"),
)


class Ordered(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    sousTotal = models.PositiveIntegerField()
    reduction = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    Ordered_Etat = models.CharField(max_length=50, choices=ORDER_ETAT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Ordered " + str(self.id)


class BillingAddress(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    prenom = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)
    numero_de_telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=200)
    seconde_adresse = models.CharField(max_length=50)
    pays = CountryField(multiple=False, null=True, blank=True)
    code_postal = models.CharField(max_length=20)
    entreprise = models.CharField(max_length=50)

    def __str__(self):
        return self.nom


class Payment(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.timestamp)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount_coupon = models.FloatField(default=0)

    def __str__(self):
        return self.code

# TEst
