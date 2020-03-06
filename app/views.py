from django.shortcuts import render

import uuid

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,CreateAPIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

from app.serializers import UserSerializer,BlogSerializer
from app.models import UserModel,Blog

# Create your views here.

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
    # 查询集
    queryset = Blog.objects.all()

    def get_user(self):
        try:
            token = self.request.query_params.get('token')

            user_id = cache.get(token)

            #
            user = UserModel.objects.get(pk=user_id)
        except Exception as e:
            print(e)
            raise  APIException(detail='用户信息不存在', code=status.HTTP_400_BAD_REQUEST)
        return user
    # 获取
    def get(self, request, *args, **kwargs):

        user = self.get_user()

        return self.list(request, *args, **kwargs)
    # 添加
    def post(self, request, *args, **kwargs):

        user = self.get_user()

        return self.create(request, *args, **kwargs)

    


'''
class TokenView(APIView):
    def get(self,request, *args, **kwargs):
        # 通过url接受参数
        token = request.query_params.get('token')
        if not token:
            return Response({'code':403, 'error':'请先登录'})

        return Response('token验证成功')
'''









