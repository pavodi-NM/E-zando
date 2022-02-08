from django.urls import path

from . import views
from .views import chatroom
app_name = "chat"
urlpatterns = [
    path('chat-room/<int:pk>/<slug:slug>/', chatroom, name='chat-room'),
    path("ajax/<int:pk>/<slug:slug>/", views.ajax_load_messages, name="chatroom-ajax"),
   # path('<str:room_name>/', views.room, name='room'),
]