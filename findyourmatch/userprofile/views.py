
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import UserProfile, UserLike, UserInteractions, UserAccountSettings, Category, Interest, Language
from .serializers import (
    UserProfileSerializer,
    UserInteractionSerializer,
    UserLikeSerializer,
    UserAccountSettingSerializer, CategorySerializer, InterestSerializer,
    LanguageSerializer
)
# Create your views here.


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing user profiles
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Allow users to only access their profile.
        """
        user = self.request.user

        if user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)
    

    def create(self, request, *args, **kwargs):
        if UserProfile.objects.filter(user=self.request.user).exists():
            return Response({'detail': 'UserProfile already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
    

    @action(detail=False, methods=['patch'], url_path='me')
    def update_me(self, request):
        profile = UserProfile.objects.get(user=self.request.user)
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    



class UserInteractionsViewSet(viewsets.ModelViewSet):
    """
    API for user Interactions
    """

    queryset = UserInteractions.objects.all()
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        """
        Return Interactions for the logged-in user
        """
        return UserInteractions.objects.filter(user=self.request.user)
    


class UserLikeViewSet(viewsets.ModelViewSet):
    """
    API for user likes
    """

    queryset = UserLike.objects.all()
    serializer_class = UserLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return Likes given/received by the logged-in user
        """

        return UserLike.objects.filter(user=self.request.user)


class UserAccountSettingsViewSet(viewsets.ModelViewSet):
    """
    API for user account settings.
    """
    queryset = UserAccountSettings.objects.all()
    serializer_class = UserAccountSettingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Allow users to update their own account settings.
        """
        return UserAccountSettings.objects.filter(user=self.request.user)



class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class CategoryRetriveDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]



class InterestListCreateView(generics.ListCreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAdminUser]


class InterestRetriveDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interest.objects.all()   
    serializer_class = InterestSerializer
    permission_classes = [permissions.IsAdminUser]



class LanguageListCreateView(generics.ListCreateAPIView):
    queryset = Language.objects.all()   
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAdminUser]



