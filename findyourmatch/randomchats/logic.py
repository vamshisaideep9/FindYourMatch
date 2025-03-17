import random
import redis
import json
from django.db.models import Q
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from .models import ChatSession

User = get_user_model()


redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

async def find_random_chat_partner(consumer):
    """Finds a random online user and connects them to a chat."""
    user_id = str(consumer.user.id)
    available_users = redis_client.smembers("online_users")
    
    # Remove self from the list
    available_users.discard(user_id)

    if available_users:
        # Pick a random user
        partner_id = random.choice(list(available_users))
        
        # Get or create chat room
        chat_room = await sync_to_async(ChatSession.get_or_create_room)(consumer.user, User.objects.get(id=int(partner_id)))

        consumer.partner_id = partner_id  # Store the matched user's ID
        consumer.chat_room_name = f"chat_{chat_room.id}"

        # Add both users to the same WebSocket chat group
        await consumer.channel_layer.group_add(consumer.chat_room_name, consumer.channel_name)

        # Notify both users
        await consumer.send(json.dumps({"message": f"Connected with User {partner_id}"}))
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            consumer.chat_room_name, {"type": "chat_message", "message": "User connected!"}
        )

    else:
        await consumer.send(json.dumps({"message": "Waiting for someone to join..."}))