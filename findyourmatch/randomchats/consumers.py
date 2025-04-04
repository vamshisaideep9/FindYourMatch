import json
import time
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from redis.asyncio import Redis as AsyncRedis
from django.db import models, IntegrityError
from .models import ChatSession, Message

User = get_user_model()

POP_TWO_LUA = """
local len = redis.call('LLEN', KEYS[1])
if tonumber(len) >= 2 then
    local first = redis.call('LPOP', KEYS[1])
    local second = redis.call('LPOP', KEYS[1])
    return {first, second}
else
    return {}
end
"""

class RandomChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redis = None
        self.session = None
        self.group_name = None
        self.joined = False  # Flag to prevent duplicate group joins
        self.last_message_time = 0  # For simple rate limiting

    async def connect(self):
        self.group_name = None
        self.joined = False
        self.session = None

        self.user = self.scope['user']
        if not self.user.is_authenticated:
          
            await self.close()
            return

        try:
            self.redis = await AsyncRedis.from_url('redis://localhost:6379', decode_responses=True)
            await self.redis.set(f"user_channel:{self.user.id}", self.channel_name)
        
        except Exception as e:
            await self.close()
            return

        existing_session = await self.get_existing_session()
        if existing_session:
            await self.end_session(existing_session)
    
        await self.accept()
        if not await self.is_user_in_queue():
            await self.add_to_waiting_queue()
        await self.attempt_pairing()

    async def disconnect(self, close_code):
        if self.group_name and self.session:
            if self.joined:
                await self.channel_layer.group_discard(self.group_name, self.channel_name)
            session_id = self.session.id
            other_user = await self.get_other_user(self.session)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "user_left",
                    "username": self.user.username,
                    "session_id": session_id,
                    "message": f"{self.user.username} disconnected. Session ended.",
                    "other_user": other_user.username if other_user else None
                }
            )
            await self.end_session(self.session)
            self.session = None
            self.group_name = None

        if self.redis:
                await self.redis.delete(f"user_channel:{self.user.id}")
                if await self.is_user_in_queue():
                    await self.redis.lrem('waiting_queue', 0, str(self.user.id))
                await self.redis.close()
          
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            if not message:
                return
            
            now = time.time()
            if now - self.last_message_time < 0.5:
                await self.send(text_data=json.dumps({"message": "You're sending messages too quickly!"}))
                return
            self.last_message_time = now

            if not self.session or not await self.is_session_active(self.session):
                await self.send(text_data=json.dumps({"message": "No one to chat with yet! Waiting for a match."}))
                return

            await self.save_message(message)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": self.user.username,
                    "session_id": self.session.id
                }
            )
        except json.JSONDecodeError as e:
            await self.send(text_data=json.dumps({"message": "Invalid message format"}))



    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        session_id = event["session_id"]
        await self.send(text_data=json.dumps({
            "event": "message",
            "message": message,
            "username": username,
            "session_id": session_id
        }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            "event": "user_left",
            "username": event["username"],
            "session_id": event["session_id"],
            "message": event["message"],
            "other_user": event["other_user"]
        }))

    async def user_paired(self, event):
        await self.send(text_data=json.dumps({
            "event": "paired",
            "usernames": event["usernames"],
            "session_id": event["session_id"],
            "message": event["message"]
        }))

    async def add_to_waiting_queue(self):
        try:
            await self.redis.rpush('waiting_queue', str(self.user.id))
            await self.send(text_data=json.dumps({"message": "In waiting room... looking for a match."}))
        except Exception as e:
            await self.send(text_data=json.dumps({"message": "Error joining queue"}))

    async def attempt_pairing(self):
        lock_key = "pairing_lock"
        try:
            got_lock = await self.redis.set(lock_key, self.user.id, nx=True, ex=5)
            if not got_lock:
                return

            popped = await self.redis.eval(POP_TWO_LUA, 1, 'waiting_queue')
            if len(popped) < 2:
                for uid in popped:
                    await self.redis.rpush('waiting_queue', uid)
                return

            user1_id, user2_id = int(popped[0]), int(popped[1])

            if self.user.id not in (user1_id, user2_id):
                await self.redis.rpush('waiting_queue', str(user1_id))
                await self.redis.rpush('waiting_queue', str(user2_id))
                return

            other_user_id = user2_id if self.user.id == user1_id else user1_id
            other_user = await self.get_user_by_id(other_user_id)
            if not other_user:
                await self.redis.rpush('waiting_queue', str(self.user.id))
                return
            existing = await self.get_existing_session_for_users(other_user)
            if existing and await self.is_session_active(existing):
                self.session = existing
                self.group_name = f"chat_{self.session.id}"
                return

            self.session = await self.create_chat_session(other_user)
            self.group_name = f"chat_{self.session.id}"

            user1_channel = await self.redis.get(f"user_channel:{min(self.user.id, other_user.id)}")
            user2_channel = await self.redis.get(f"user_channel:{max(self.user.id, other_user.id)}")
            if user1_channel and user2_channel:
                for channel, uid in ((user1_channel, min(self.user.id, other_user.id)),
                                     (user2_channel, max(self.user.id, other_user.id))):
                    await self.channel_layer.send(
                        channel,
                        {
                            "type": "set_session",
                            "session_id": self.session.id,
                            "group_name": self.group_name,
                            "user_id": uid
                        }
                    )
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "user_paired",
                        "usernames": [self.user.username, other_user.username],
                        "session_id": self.session.id,
                        "message": f"Matched! {self.user.username} and {other_user.username} are now chatting."
                    }
                )
        
            else:
                await self.end_session(self.session)
                await self.redis.rpush('waiting_queue', str(self.user.id))
        
        except Exception as e:
       
            if self.session:
                await self.end_session(self.session)
        finally:
            await self.redis.delete(lock_key)

    async def set_session(self, event):
        """Set session details and join the group, ensuring every consumer joins."""
        self.group_name = event["group_name"]
        self.session = await self.get_session_by_id(event["session_id"])
        if self.session:
            if not self.joined:
                await self.channel_layer.group_add(self.group_name, self.channel_name)
                self.joined = True
   
            else:
                print(f"{self.user.username} already joined group {self.group_name}")
        else:
            await self.send(text_data=json.dumps({"message": "Session not found"}))

    async def is_user_in_queue(self):
        try:
            queue = await self.redis.lrange('waiting_queue', 0, -1)
            return str(self.user.id) in queue
        except Exception as e:
            return False

    @database_sync_to_async
    def get_existing_session(self):
        return ChatSession.objects.filter(
            models.Q(user1=self.user) | models.Q(user2=self.user),
            active=True
        ).first()

    @database_sync_to_async
    def get_existing_session_for_users(self, other_user):
        user_ids = sorted([self.user.id, other_user.id])
        return ChatSession.objects.filter(
            user1_id=user_ids[0],
            user2_id=user_ids[1]
        ).first()

    @database_sync_to_async
    def get_existing_session_for_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            return ChatSession.objects.filter(
                models.Q(user1=user) | models.Q(user2=user)
            ).first()
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_session_by_id(self, session_id):
        try:
            return ChatSession.objects.select_related('user2').get(id=session_id)
        except ChatSession.DoesNotExist:
            return None

    @database_sync_to_async
    def is_session_active(self, session):
        return session.user2 is not None and getattr(session, 'active', True)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_other_user(self, session):
        return session.user2 if session.user1 == self.user else session.user1

    @database_sync_to_async
    def create_chat_session(self, other_user):
        user_ids = sorted([self.user.id, other_user.id])
        user1 = User.objects.get(id=user_ids[0])
        user2 = User.objects.get(id=user_ids[1])
        try:
            return ChatSession.objects.create(user1=user1, user2=user2, active=True)
        except IntegrityError:
            existing = ChatSession.objects.get(user1_id=user_ids[0], user2_id=user_ids[1])
            if not existing.active:
                existing.active = True
                existing.save()
            return existing

    @database_sync_to_async
    def save_message(self, message):
        Message.objects.create(chat_session=self.session, sender=self.user, content=message)

    @database_sync_to_async
    def end_session(self, session):
        if session:
            session.active = False
            session.save()
        else:
           print("Attempted to end a None session")
