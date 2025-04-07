from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q
from enum import Enum

User = get_user_model()

# Create your models here.



class GenderChoices(Enum):
    MALE = "Male"
    FEMALE = "Female"
    NON_BINARY = "Non-Binary"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").capitalize()) for choice in cls]
    



class SmokingChoices(Enum):
    NEVER = "Never"
    REGULARLY = "Regularly"
    SOCIALLY = "Socially"
    TRYING_TO_QUIT = "Trying to Quit"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").capitalize()) for choice in cls]
    


class DrinkingChoices(Enum):
    NEVER = "Never"
    REGULARLY = "Regularly"
    SOCIALLY = "Socially"
    TRYING_TO_QUIT = "Trying to Quit"


    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").capitalize()) for choice in cls]
    


class EthnicityChoices(Enum):
    ASIAN = "Asian"
    BLACK = "Black"
    CAUCASIAN = "Caucasian"
    HISPANIC = "Hispanic"
    MIDDLE_EASTERN = "Middle Eastern"
    MIXED = "Mixed"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").capitalize()) for choice in cls]



class ReligionChoices(Enum):
    CHRISTIANITY = "Christianity"
    ISLAM = "Islam"
    HINDUISM = "Hinduism"
    BUDDHISM = "Buddhism"
    JUDAISM = "Judaism"
    ATHEIST = "Atheist"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").capitalize()) for choice in cls]


class RelationshipGoalsChoices(Enum):
    CASUAL = "Casual Dating"
    SERIOUS = "Serious Relationship"
    MARRIAGE = "Marriage"
    FRIENDS = "Friendship"
    NOT_SURE = "Not Sure"

    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").capitalize()) for choice in cls]


class AccountStatus(Enum):
    ACTIVE = "Active"
    PAUSED = "Paused"
    BANNED = "Banned"


    @classmethod
    def choices(cls):
        return [(choice.value, choice.name.replace("_", " ").capitalize()) for choice in cls]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=50, unique=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="interests", default=12)
    def __str__(self):
        return self.name
    

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    display_name = models.CharField(max_length=30, null=True, blank=True, unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    

    #personal-info
    gender = models.CharField(max_length=10, choices=GenderChoices.choices(), blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    height_feet = models.IntegerField(null=True, blank=True)
    height_inches = models.IntegerField(null=True, blank=True)
    ethnicity = models.CharField(max_length=50, choices=EthnicityChoices.choices(), blank=True, null=True)
    religion = models.CharField(max_length=50, choices=ReligionChoices.choices(), blank=True, null=True)
    languages_spoken = models.ManyToManyField(Language, related_name="speakers", blank=True)
    current_location = models.CharField(max_length=100, blank=True, null=True)
    native_place = models.CharField(max_length=100, blank=True, null=True)


    #preferences
    interested_in = models.CharField(max_length=10, choices=GenderChoices.choices(), blank=True, null=True)
    relationship_goals = models.CharField(
        max_length=30, choices=RelationshipGoalsChoices.choices(), null=True, blank=True
    )
    interests = models.ManyToManyField(Interest, related_name="user_profiles", blank=True)
    age_preference_min = models.IntegerField(default=18, validators=[MinValueValidator(18), MaxValueValidator(99)])
    age_preference_max = models.IntegerField(default=99, validators=[MinValueValidator(18), MaxValueValidator(99)])
    distance_preference = models.IntegerField(default=50)


    #life style
    education = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    smoking = models.CharField(max_length=30, choices=SmokingChoices.choices(), null=True, blank=True)
    drinking = models.CharField(max_length=30, choices=DrinkingChoices.choices(), null=True, blank=True)


    def __str__(self):
        return self.display_name if self.display_name else f"User {self.user.id}"
    


class UserInteractions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_interactions")
    likes = models.ManyToManyField(
        "UserProfile", through="UserLike", related_name="liked_by", blank=True
    )
    is_online = models.BooleanField(default=False)

    def get_matches(self):
        """Get mutual likes (matches) dynamically."""
        return UserProfile.objects.filter(
        liked_by__user_interactions__user=self.user 
        ).filter(user_interactions_likes=self.user.user_profile)

    def __str__(self):
        return f"Interactions of {self.user.email}"


class UserLike(models.Model):
    user_interactions = models.ForeignKey(UserInteractions, on_delete=models.CASCADE)
    liked_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user_interactions", "liked_profile")

    def __str__(self):
        return f"{self.user_interactions.user.email} liked {self.liked_profile.display_name}"


class UserAccountSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_account_settings")
    account_status = models.CharField(max_length=30, choices=AccountStatus.choices(), blank=True, null=True, default=AccountStatus.ACTIVE.value)
    is_verified = models.BooleanField(default=False)
    last_seen = models.DateTimeField(auto_now=True)



    






