from django.contrib import admin
from .models import ChatSession, Message

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user1", "user2", "created_at")
    search_fields = ("user1__username", "user2__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_session", "sender", "content", "timestamp")
    search_fields = ("sender__username", "content")
    list_filter = ("timestamp",)
    ordering = ("-timestamp",)
