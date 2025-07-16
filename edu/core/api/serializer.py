from rest_framework import serializers
from core.models import Resource, HelpForm, SiteSettings, CustomUser
from django.contrib.auth.password_validation import validate_password

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def validate(self, data):
        validate_password(data["password"])
        return data
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        user = CustomUser.objects.create_user(
            username = username,
            password = password
        )
        return user

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"

class HelpFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpForm
        fields = "__all__"

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"
