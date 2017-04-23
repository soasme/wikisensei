# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from .models import Option

class ProfileSettingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = (
            'private_wiki',
            'private_email',
        )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            'private_email': instance.private_email,
            'private_wiki': instance.private_wiki,
        }

    @classmethod
    def get_option_by_user(self, user):
        try:
            return user.option
        except Option.DoesNotExist:
            option = Option(user=user)
            option.save()
            return option
