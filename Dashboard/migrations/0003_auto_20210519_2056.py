# Generated by Django 3.1.7 on 2021-05-19 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_auto_20210518_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendeurbusiness',
            name='mode_payement_accepte',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
