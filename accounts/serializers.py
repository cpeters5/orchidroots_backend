from rest_framework import serializers
from .models import *
from django.utils.translation import ugettext as _


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('pk', 'country')


class PhotographerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photographer
        fields = ('author_id', 'displayname')


class ProfileSerializer(serializers.ModelSerializer):
    current_credit_name_id = serializers.PrimaryKeyRelatedField(
        write_only=True, required=False, allow_null=True, default=None, source='current_credit_name', queryset=Photographer.objects.all())

    class Meta:
        model = Profile
        fields = ('photo_credit_name', 'specialty',
                  'country', 'current_credit_name_id',)

    def validate_current_credit_name_id(self, data):
        if data and Profile.objects.filter(current_credit_name=data).count():
            raise serializers.ValidationError(
                'This credit name has already been taken!')
        return data


class SignupSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(write_only=True)
    confirm_password = serializers.CharField(max_length=256)

    class Meta:
        model = User
        exclude = ('reset_pass_code',)

    def create(self, validated_data):
        profile_dict = validated_data.pop('profile', None)
        user = User.objects.create(**validated_data)
        profile_dict['user'] = user
        profile = Profile.objects.create(**profile_dict)
        return user

    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError(
                "This password is too short. It must contain at least 8 characters.")
        if not data['confirm_password'] == data['password']:
            raise serializers.ValidationError(
                "confirmed password doesn't match your password")
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)


class VerifyEmailCodeApiSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=5)


class ResendVerifyEmailCodeApiSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgetPasswordSendEmailCodeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)


class ResetPasswordVerifyCodeApiSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    code = serializers.CharField(max_length=5)


class RestPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    code = serializers.CharField(max_length=5)
    new_password = serializers.CharField(max_length=256)


class SocialLoginSerializer(serializers.Serializer):
    social_type = serializers.CharField(max_length=256)
    social_token = serializers.CharField(max_length=300)
    social_id = serializers.CharField(max_length=256)

    def validate(self, data):
        if not data['social_type'] in ['facebook']:
            raise serializers.ValidationError(
                "social_type can only be 'facebook'")
        return data