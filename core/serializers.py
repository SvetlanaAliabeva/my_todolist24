from typing import Any, Type

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User



from django.core.exceptions import ValidationError
from rest_framework import serializers

from core.models import User
from todolist.fields import PasswordField

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        required=True,
        write_only=True
    )
    password_repeat = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs) -> Any:
        if attrs.get('password') != attrs.pop('password_repeat'):
            raise serializers.ValidationError('Password mismatch')
        validate_password(attrs.get('password'))
        return attrs

    def create(self, validated_data) -> Any:
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model: Type[User] = User
        fields: tuple = ('username', 'password_repeat', 'password')


#
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
#
#
# class CreateUserSerializer(serializers.ModelSerializer):
#     password = PasswordField(required=True, write_only=False)
#     password_repeat = PasswordField(required=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')
#
#     def validate(self, attrs: dict) -> dict:
#         if attrs['password'] != attrs['password_repeat']:
#             raise ValidationError('Password must match')
#         return attrs
#
#
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = PasswordField(required=True)
#
#
# class UpdatePasswordSerializer(serializers.Serializer):
#     old_password = PasswordField(required=True)
#     new_password = PasswordField(required=True)

