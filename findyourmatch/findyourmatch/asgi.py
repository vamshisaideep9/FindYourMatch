"""
ASGI config for findyourmatch project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "findyourmatch.settings")
django.setup()  # Ensures Django loads the apps before importing anything

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from randomchats.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": URLRouter(websocket_urlpatterns),
})