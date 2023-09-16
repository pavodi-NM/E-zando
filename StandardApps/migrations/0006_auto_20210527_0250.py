# Generated by Django 3.1.7 on 2021-05-26 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StandardApps', '0005_souscategory_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandeStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('status', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='commande_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='StandardApps.commandestatus'),
        ),
    ]
