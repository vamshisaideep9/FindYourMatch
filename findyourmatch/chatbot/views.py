import random
import json
import os
import time
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from celery.result import AsyncResult
from .models import AmoraQuestion, UserInterestResponse
from userprofile.models import Category, Interest, UserProfile
from .serializers import AmoraQuestionSerializer, UserInterestResponseSerializer
from chatbot.tasks import select_categories_for_user
from dotenv import load_dotenv
load_dotenv()

LANGSMITH_TRACING=os.getenv("LANGSMITH_TRACKING")
LANGSMITH_ENDPOINT=os.getenv("LANGSMITH_ENDPOINT")
LANGSMITH_API_KEY=os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT=os.getenv("LANGSMITH_PROJECT")


class AmoraQuestionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        questions = list(AmoraQuestion.objects.all())
        random.shuffle(questions)
        selected_questions = questions[:10]
        serializer = AmoraQuestionSerializer(selected_questions, many=True)
        return Response(serializer.data)

class UserInterestResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        answers = request.data.get("answers", [])

        for answer in answers:
            question = AmoraQuestion.objects.get(id=answer["question_id"])
            response = answer["response"]
            UserInterestResponse.objects.update_or_create(
                user=user, question=question, defaults={"response": response}
            )

        return Response({"message": "Responses saved successfully!"}, status=status.HTTP_201_CREATED)



class UserCategoryRecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        categories = select_categories_for_user(user.id) 
        return Response({"categories": categories, "message": "Processing completed successfully."})
    
class UserInterestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        categories = select_categories_for_user(user.id)
        
        if not categories:
            return Response({"message": "No categories found for the user."}, status=404)
        
        categorized_interests = {}

        for category_name in categories:
            interests = Interest.objects.filter(category__name=category_name).values_list("name", flat=True)
            categorized_interests[category_name] = list(interests)

        return Response({
            "interests": categorized_interests, 
            "message": "Interests Fetched Successfully."
        })
    


class SaveUserInterestsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        selected_interests = request.data.get("selected_interests", [])
        if not selected_interests:
            return Response({"error": "No interests selected."}, status=400)
        interests_qs = Interest.objects.filter(name__in=selected_interests)
        if not interests_qs.exists():
            return Response({"error": "Invalid interests selected."}, status=400)
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.interests.set(interests_qs)  

        return Response({"message": "User interests saved successfully."}, status=200)