from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'first_name', 'last_name',
                  'phone_number', 'address', 'email', 'password', 'profile_picture']
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone_number": {"required": True},
            "address": {"required": True},
            "password": {"required": True},
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
