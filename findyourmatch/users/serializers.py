from rest_framework import serializers
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')

# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            verification_link = f"http://127.0.0.1:8000/api/auth/verify-email/{uid}/{token}/"

            send_mail(
                "Verify Your Email",
                f"Click the link to verify your email: {verification_link}",
                "no-reply@yourdomain.com",
                [value],
            )
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://localhost:8000/api/auth/reset-password/{uid}/{token}/"

            send_mail(
                "Password Reset Request",
                f"Click the link to reset your password: {reset_link}",
                "no-reply@yourdomain.com",
                [value],
            )
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data["uidb64"]))
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, data["token"]):
                raise serializers.ValidationError("Invalid or expired token")

            user.set_password(data["new_password"])
            user.save()
            return data
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError("Invalid user")
        


import random
import string

def generate_username():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class UsernameResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
            new_username = generate_username()
            user.username = new_username
            user.save()

            send_mail(
                "Username Reset",
                f"Your new username is: {new_username}",
                "no-reply@yourdomain.com",
                [value],
            )
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")

