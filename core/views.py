from typing import Any

from django.contrib.auth import authenticate, login
from django.shortcuts import render
from requests import Request
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from core.models import User
from core.serializer import UserRegistrationSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().post(request, *args, **kwargs)


class UserLoginView(CreateAPIView):
    def post(self, request: Request, *args: tuple, **kwargs: dict) -> Response:

        user: Any = authenticate(
            username=request.data.get('username'),
            password=request.data.get('password')
        )
        if user:
            login(request, user)
            return Response('Successful login', status=status.HTTP_200_OK)
        raise AuthenticationFailed('Invalid username or password')
