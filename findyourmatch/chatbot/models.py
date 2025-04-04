from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class AmoraQuestion(models.Model):
    text = models.TextField(unique=True)

    def __str__(self):
        return self.text
    


class UserInterestResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interest_response")
    question = models.ForeignKey(AmoraQuestion, on_delete=models.CASCADE)
    response = models.BooleanField()

    class Meta:
        unique_together = ("user", "question")

    def __str__(self):
        return f"{self.user.username} - {self.question.text}: {'Yes' if self.response else 'No'}"
