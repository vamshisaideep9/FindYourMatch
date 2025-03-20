from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/random_chat/", consumers.RandomChatConsumer.as_asgi()),
]