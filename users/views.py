from rest_framework import viewsets
from django.shortcuts import render

from users.models import User
from users.serializers import UserFullSerializer, UserPartialSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPartialSerializer

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return UserFullSerializer
        return UserPartialSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        return super().perform_create(user)


