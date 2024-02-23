from rest_framework import serializers

from users.models import User


class UserFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
