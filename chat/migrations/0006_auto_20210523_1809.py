# Generated by Django 3.1.7 on 2021-05-23 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_vendeurmessages_sender'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientmessages',
            options={'ordering': ('timestamp',)},
        ),
        migrations.AlterModelOptions(
            name='vendeurmessages',
            options={'ordering': ('timestamp',)},
        ),
    ]
