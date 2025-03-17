from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class ChatSession(models.Model):
    user1 = models.ForeignKey(User, related_name="chat_sessions1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="chat_sessions2", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    disconnected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"
    

    @staticmethod
    def get_or_create_room(user1, user2):
        """
        Ensure a unique chat room exists for two users
        """
        room, created - ChatSession.objects.get_or_create(
            user1=min(user1, user2, key=lambda x: x.id),
            user2=max(user1, user2, key=lambda x: x.id),
        )
        return room
    
    


class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}"