from rest_framework import serializers
from .models import Account


class AccountUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'address']
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone_number": {"required": True},
            "address": {"required": True},
        }


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name',
                  'phone_number', 'address', 'email', 'password', 'profile_picture', "is_superuser"]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone_number": {"required": True},
            "address": {"required": True},
            "password": {"required": True},
            "is_superuser": {"required": False},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is None:
            raise serializers.ValidationError("Password is required")
        user = self.Meta.model(**validated_data)

        if password is not None:
            user.set_password(password)
        user.save()
        return user
