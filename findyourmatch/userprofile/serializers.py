from rest_framework import serializers
from .models import (
    UserProfile, UserInteractions, UserLike, UserAccountSettings, Interest, Language
)
from .helper_functions import get_enum_choices
from .models import (
    GenderChoices, SmokingChoices, DrinkingChoices, PetChoices, EthnicityChoices,
    ReligionChoices, RelationshipGoalsChoices, AccountStatus, Category
)



class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    gender = serializers.ChoiceField(choices=get_enum_choices(GenderChoices))
    interested_in = serializers.ChoiceField(choices=get_enum_choices(GenderChoices))
    ethnicity = serializers.ChoiceField(choices=get_enum_choices(EthnicityChoices))
    religion = serializers.ChoiceField(choices=get_enum_choices(ReligionChoices))
    relationship_goals = serializers.ChoiceField(choices=get_enum_choices(RelationshipGoalsChoices))
    smoking = serializers.ChoiceField(choices=get_enum_choices(SmokingChoices), required=False)
    drinking = serializers.ChoiceField(choices=get_enum_choices(DrinkingChoices), required=False)
    pets = serializers.ChoiceField(choices=get_enum_choices(PetChoices), required=False)


    interests = serializers.SlugRelatedField(
        many=True, queryset=Interest.objects.all(), slug_field="name"
    )

    languages_spoken = serializers.SlugRelatedField(
        many=True, queryset=Language.objects.all(), slug_field="name"
    )


    class Meta:
        model = UserProfile
        fields = "__all__"

    def get_serializer_context(self):
        """
        Ensure the serializer receives request context.
        """
        return {"request": self.request}


    def create(self, validated_data):
        """
        Custom create method to handle many-to-many fields properly.
        """
        interests = validated_data.pop("interests", [])
        languages_spoken = validated_data.pop("languages_spoken", [])
        
        validated_data["user"] = self.context["request"].user  
        user_profile = super().create(validated_data)

        user_profile.interests.set(interests)
        user_profile.languages_spoken.set(languages_spoken)
        
        return user_profile
    
    def update(self, instance, validated_data):
        """
        Custom update method to handle many-to-many fields properly.
        """
        interests = validated_data.pop("interests", None)
        languages_spoken = validated_data.pop("languages_spoken", None)

        instance = super().update(instance, validated_data)

        if interests is not None:
            instance.interests.set(interests)
        if languages_spoken is not None:
            instance.languages_spoken.set(languages_spoken)

        return instance





class UserInteractionSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()

    class Meta:
        model = UserInteractions
        fields = ["user", "likes", "is_online", "matches"]


    def get_matches(self, obj):
        """ Fetch mutual matches for the user """

        return UserProfileSerializer(obj.get_matches(), many=True).data


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLike
        fields = "__all__"



class UserAccountSettingSerializer(serializers.ModelSerializer):
    account_status = serializers.ChoiceField(choices=get_enum_choices(AccountStatus))

    class Meta:
        model = UserAccountSettings
        fields = ["user", "account_status", "is_verified", "last_seen"]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"



class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = "__all__"


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"