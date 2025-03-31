from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    UserInteractionsViewSet,
    UserLikeViewSet,
    UserAccountSettingsViewSet,
    InterestRetriveDeleteView, InterestListCreateView,
    CategoryListCreateView, CategoryRetriveDeleteView,
    LanguageListCreateView
)


urlpatterns = [
    path("user-profile/", UserProfileViewSet.as_view({'get':'list', 'post': 'create'}), name="user-profile"),
    path("Account/", UserAccountSettingsViewSet.as_view({'get':'list'}), name="user-account"),
    path("interests/", InterestListCreateView.as_view(), name="interest-list-create"),
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("languages/", LanguageListCreateView.as_view(), name="language-list-create")
]
