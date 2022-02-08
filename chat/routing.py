
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # sending the web socket request
    re_path(r'wss/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer),
]