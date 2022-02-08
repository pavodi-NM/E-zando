# Generated by Django 4.0.2 on 2022-02-08 18:50

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VendeurBusiness',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_business', models.CharField(default='bilocost', max_length=100)),
                ('type_business', models.CharField(default='detaillant', max_length=50)),
                ('categorie_choses_vendues', models.CharField(default='electroniques', max_length=200)),
                ('lieu_physique_shop', models.CharField(default='Kinshasa', max_length=200)),
                ('pays', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('mode_payement_accepte', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VendorPolitique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('politique', models.CharField(default='agree', max_length=200)),
            ],
        ),
    ]
