from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

from StandardApps.models import Clients, Vendeurs, Produits
from .models import User, Message
from django.db.models import Q
import json


# Create your views here.

def room(request, room_name):
    return render(request, 'chatroom/chat-room.html', {
        'room_name': room_name
    })


def chatroom(request, pk, slug):
    # client as the current user
    current_user = request.user
    print(current_user)
    current_client = Clients.objects.get(user=current_user)
    # get the selected product
    product_slug = Produits.objects.get(slug=slug)
    # current vendor
    current_vendeur = Vendeurs.objects.get(pk=pk)
    print(product_slug)
    messages = Message.objects.filter(
        Q(receiver=current_vendeur, sender=current_client, produit=product_slug)
    )
    messages.update(seen=True)
    messages = messages | Message.objects.filter(Q(receiver=current_vendeur, sender=current_client,produit=product_slug))
    return render(request, "chatroom-sample.html",
                  {"other_user": current_vendeur, "messages": messages,
                   "product_slug":product_slug, "client":current_client})


def ajax_load_messages(request, pk, slug):
    # get the current product vendor
    current_vendeur = Vendeurs.objects.get(pk=pk)
    # get the product
    produit_slug = Produits.objects.get(slug=slug)

    current_user = request.user
    current_client = Clients.objects.get(user=current_user)
    messages = Message.objects.filter(seen=False).filter(
        Q(receiver=current_vendeur, sender=current_client)
    )

    message_list = [{
        "sender": message.sender,
        "message": message.message,
        "sent": message.sender.user == request.user
    } for message in messages]
    messages.update(seen=True)

    if request.method == "POST":
        current_client = Clients.objects.get(user=current_user)
        message = json.loads(request.body)
        m = Message.objects.create(receiver=current_vendeur, sender=current_client,
                                   owner_message=current_user,produit=produit_slug,
                                   message=message)
        message_list.append({
            "sender": current_client.user.username,
            "message": m.message,
            "sent": True,
        })
        print(m)
    print(message_list)
    return JsonResponse(message_list, safe=False)