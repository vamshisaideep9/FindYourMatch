from rest_framework import serializers
from .models import AmoraQuestion, UserInterestResponse

class AmoraQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmoraQuestion
        fields = ["id", "text"]

class UserInterestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterestResponse
        fields = ["user", "question", "response"]
