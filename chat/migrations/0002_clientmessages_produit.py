# Generated by Django 3.1.7 on 2021-05-22 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StandardApps', '0004_category_descriptioncategory'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientmessages',
            name='produit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='StandardApps.produits'),
        ),
    ]
