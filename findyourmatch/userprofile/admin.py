from django.contrib import admin
from .models import (
    Category, Interest, Language, UserProfile, UserInteractions, UserLike, UserAccountSettings
)

# Inline for UserLike in UserInteractions
class UserLikeInline(admin.TabularInline):
    model = UserLike
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "display_name", "gender", "date_of_birth", "current_location")
    list_filter = ("gender", "ethnicity", "religion", "relationship_goals")
    search_fields = ("user__email", "display_name", "current_location", "native_place")
    ordering = ("user",)
    filter_horizontal = ("languages_spoken", "interests")

@admin.register(UserInteractions)
class UserInteractionsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "is_online")
    search_fields = ("user__email",)
    inlines = [UserLikeInline]

@admin.register(UserLike)
class UserLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user_interactions", "liked_profile", "liked_at")
    search_fields = ("user_interactions__user__email", "liked_profile__display_name")
    list_filter = ("liked_at",)
    ordering = ("-liked_at",)

@admin.register(UserAccountSettings)
class UserAccountSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "account_status", "is_verified", "last_seen")
    list_filter = ("account_status", "is_verified")
    search_fields = ("user__email",)
    ordering = ("-last_seen",)
