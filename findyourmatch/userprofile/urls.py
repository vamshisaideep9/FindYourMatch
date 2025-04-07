from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    UserAccountSettingsViewSet,
   InterestListCreateView,
    CategoryListCreateView, 
    LanguageListCreateView
)


router = DefaultRouter()
router.register(r'user-profile', UserProfileViewSet, basename="user-profile")
router.register(r'account', UserAccountSettingsViewSet, basename='account')



urlpatterns = [
    path('', include(router.urls)),
    path("interests/", InterestListCreateView.as_view(), name="interest-list-create"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("languages/", LanguageListCreateView.as_view(), name="language-list-create")
]
