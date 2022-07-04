from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from medical.serializers import DiagnosisSerializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "gender",
            "birth_date",
        ]
        extra_kwargs = {"gender": {"required": True}, "birth_date": {"required": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            gender=validated_data["gender"],
            birth_date=validated_data["birth_date"],
        )

        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    diagnostics = DiagnosisSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "first_name",
            "last_name",
            "birth_date",
            "gender",
            "diagnostics",
        ]
