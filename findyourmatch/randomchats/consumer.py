import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatSession, Message
from .logic import find_random_chat_partner

User = get_user_model()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


class RandomChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        # Add user to Redis online pool
        redis_client.sadd("online_users", str(self.user.id))
        await self.accept()

        # Try to find a chat partner
        await find_random_chat_partner(self)

    async def disconnect(self, close_code):
        """Remove user from Redis and notify partner if needed."""
        redis_client.srem("online_users", str(self.user.id))

        if hasattr(self, "chat_room_name"):
            await self.channel_layer.group_discard(self.chat_room_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming messages and saves them."""
        data = json.loads(text_data)
        message = data.get("message", "")

        if hasattr(self, "chat_room_name"):
            # Save message to DB
            await self.save_message_to_db(message)

            # Send message to chat room
            await self.channel_layer.group_send(
                self.chat_room_name,
                {"type": "chat_message", "message": message, "sender": self.user.username},
            )

    async def chat_message(self, event):
        """Sends message to frontend."""
        await self.send(text_data=json.dumps({"message": event["message"], "sender": event["sender"]}))

    @database_sync_to_async
    def save_message_to_db(self, message):
        """Stores messages in the database."""
        chatroom = ChatSession.objects.get(id=int(self.chat_room_name.split("_")[1]))
        Message.objects.create(chatroom=chatroom, sender=self.user, content=message)



