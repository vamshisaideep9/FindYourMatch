from django.urls import path
from .consumer import RandomChatConsumer

websocket_urlpatterns = [
    path("ws/chat/random/", RandomChatConsumer.as_asgi()),
]
