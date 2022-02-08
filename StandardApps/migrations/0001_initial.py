# Generated by Django 3.1.7 on 2021-05-17 18:09

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=200)),
                ('nom', models.CharField(max_length=200)),
                ('numero_de_telephone', models.CharField(max_length=20)),
                ('adresse', models.CharField(max_length=200)),
                ('seconde_adresse', models.CharField(max_length=50)),
                ('pays', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('code_postal', models.CharField(max_length=20)),
                ('entreprise', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_de_reference', models.CharField(max_length=20)),
                ('total', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('en_cours_de_livraison', models.BooleanField(default=False)),
                ('livraison_recue', models.BooleanField(default=False)),
                ('demande_de_remboursement', models.BooleanField(default=False)),
                ('remboursement_accepte', models.BooleanField(default=False)),
                ('remboursement_rejete', models.BooleanField(default=False)),
                ('billing_adress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StandardApps.billingaddress')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='StandardApps.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_complet', models.CharField(blank=True, max_length=200, null=True)),
                ('adresse', models.CharField(blank=True, default='Kinshasa', max_length=200, null=True)),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('pays', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('device', models.CharField(blank=True, max_length=100, null=True)),
                ('est_client', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount_coupon', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Produits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titreProduit', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True)),
                ('imageProduit', models.ImageField(upload_to='produits')),
                ('DescriptionProduit', models.TextField(blank=True, null=True)),
                ('reduction', models.BooleanField(default=False)),
                ('prixDiscount', models.PositiveIntegerField(blank=True, null=True)),
                ('prixActual', models.PositiveIntegerField()),
                ('garantieProduit', models.CharField(blank=True, max_length=300, null=True)),
                ('specifications', models.CharField(blank=True, max_length=300, null=True)),
                ('payment_options', models.CharField(blank=True, default='Main a main', max_length=200, null=True)),
                ('returnPolicy', models.CharField(blank=True, max_length=300, null=True)),
                ('viewCount', models.PositiveIntegerField(default=0)),
                ('quantite_du_stock', models.PositiveIntegerField(default=1)),
                ('stateProd', models.CharField(blank=True, max_length=20, null=True)),
                ('est_en_stock', models.BooleanField(default=True)),
                ('date_cree', models.DateTimeField(auto_now_add=True, null=True)),
                ('est_actif', models.BooleanField(default=True)),
                ('pays', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('lieu', models.CharField(blank=True, default='Kinshasa', max_length=200, null=True)),
                ('livraison_time', models.IntegerField(default=1)),
                ('categoryProduit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.category')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('est_client', models.BooleanField(default=False)),
                ('est_vendeur', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Vendeurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(default='Ndoyi', max_length=200)),
                ('nom', models.CharField(blank=True, default='Prospere', max_length=200, null=True)),
                ('email_adresse', models.CharField(default='Swede', max_length=200)),
                ('telephone', models.CharField(blank=True, default='004476983672', max_length=200, null=True)),
                ('adresse', models.CharField(blank=True, default='Kinshasa', max_length=200, null=True)),
                ('joined', models.DateTimeField(auto_now_add=True, null=True)),
                ('pays', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('est_vendeur', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='vendeurs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SousCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=100)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.category')),
            ],
        ),
        migrations.CreateModel(
            name='RevueProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujet', models.CharField(blank=True, max_length=30, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('notes', models.IntegerField(default=1)),
                ('statut', models.CharField(choices=[('Nouveau', 'Nouveau'), ('True', 'True'), ('False', 'False')], default='Nouveau', max_length=10)),
                ('ip', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StandardApps.clients')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.produits')),
            ],
        ),
        migrations.AddField(
            model_name='produits',
            name='sousCategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StandardApps.souscategory'),
        ),
        migrations.AddField(
            model_name='produits',
            name='vendeur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StandardApps.vendeurs'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StandardApps.clients')),
            ],
        ),
        migrations.CreateModel(
            name='Ordered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_by', models.CharField(max_length=200)),
                ('shipping_address', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('sousTotal', models.PositiveIntegerField()),
                ('reduction', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
                ('Ordered_Etat', models.CharField(choices=[('Commande Recu', 'Commande Recu'), ('Commande en cours de traitement', 'Commande en cours de traitement'), ('En route', 'En route'), ('Commande delivre', 'Commande delivre'), ('Commande annule', 'Commande annule')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.cart')),
            ],
        ),
        migrations.AddField(
            model_name='clients',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CartProduit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.PositiveIntegerField(blank=True, null=True)),
                ('quantite', models.PositiveIntegerField(default=1)),
                ('sousTotal', models.PositiveIntegerField(blank=True, null=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.clients')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.produits')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.clients'),
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StandardApps.coupon'),
        ),
        migrations.AddField(
            model_name='cart',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StandardApps.payment'),
        ),
        migrations.AddField(
            model_name='cart',
            name='produits',
            field=models.ManyToManyField(to='StandardApps.CartProduit'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StandardApps.clients'),
        ),
    ]