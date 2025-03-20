from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatSession(models.Model):
    user1 = models.ForeignKey(User, related_name="chat_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="chat_user2", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)  # Add this field

    class Meta:
        db_table = 'chat_sessions'
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"


class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'

    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"