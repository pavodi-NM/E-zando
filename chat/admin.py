from django.contrib import admin

# Register your models here.
from chat.models import ClientMessages, VendeurMessages, Message


@admin.register(ClientMessages)
class AdminClientMessage(admin.ModelAdmin):
    list_display = ['client', 'sent_message', 'received_message']


@admin.register(VendeurMessages)
class AdminClientMessage(admin.ModelAdmin):
    list_display = ['vendeur', 'sent_message', 'received_message']


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'message']
