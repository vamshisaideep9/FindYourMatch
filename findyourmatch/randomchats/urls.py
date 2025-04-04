from django.urls import path
from .views import random_chat_view

urlpatterns = [
    path("random_chat/", random_chat_view, name="random_chat"),
]
