import random
from django.db.models import Q
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from .models import ChatSession
User = get_user_model()


def find_random_chat_partner(user):
    """
    Find online users who are not already in a chat with the current user
    """

    available_users = User.objects.filter(
        user_interaction__is_online=True
    ).exclude(id=user.id)


    if available_users.exists():
        random_user = random.choice(available_users)
        chat_session, created = ChatSession.objects.get_or_create(
            user1 = min(user, random_user, key=lambda x: x.id),
            user2 = max(user, random_user, key=lambda x: x.id),
        )

        return chat_session
    return None