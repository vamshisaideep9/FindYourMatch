from django.urls import path
from .views import AmoraQuestionListView, UserInterestResponseView, UserCategoryRecommendationView, UserInterestsView, SaveUserInterestsView

urlpatterns = [
    path("amora/questions/", AmoraQuestionListView.as_view(), name="amora-questions"),
    path("amora/answers/", UserInterestResponseView.as_view(), name="amora-answers"),
    path("amora/recommend-categories/", UserCategoryRecommendationView.as_view(), name="user-categories"),
    path("amora/user-interests/", UserInterestsView.as_view(), name="user-interests"),
    path("amora/select-interests/", SaveUserInterestsView.as_view(), name="selected_interests")
]