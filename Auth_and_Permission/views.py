from django.shortcuts import render

# Create your views here.


import uuid

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,CreateAPIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

from Auth_and_Permission.models import UserModel, Blog
from Auth_and_Permission.auth import UserAuthentication
from Auth_and_Permission.serializers import UserSerializer, BlogSerializer


class UserAPI(CreateAPIView):
    serializer_class = UserSerializer

    queryset = UserModel.objects.all()

    def post(self, request, *args, **kwargs):
        action =request.query_params.get('action')

        if action == 'register':
            return self.create(request, *args, **kwargs)
        elif action == 'login':
            username = request.data.get('username')
            password = request.data.get('password')

            users = UserModel.objects.filter(username=username)

            if not users.exists():
                raise APIException(detail='用户不存在', code=status.HTTP_400_BAD_REQUEST)

            user = users.first()

            if not user.verify_password(password):
                raise APIException(detail='密码错误', code=status.HTTP_400_BAD_REQUEST)

            token = uuid.uuid4().hex

            print(type(cache))

            cache.set(token, user.id, 60 * 60 * 24)

            data = {
                "msg": "ok",
                "status": status.HTTP_200_OK,
                "token": token
            }

            return Response(data)

        else:
            raise APIException(detail='提供正确的action', code=status.HTTP_400_BAD_REQUEST)

class BlogsAPIView(ListCreateAPIView):

    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    authentication_classes = (UserAuthentication,)


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(author=self.request.user)

