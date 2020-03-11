from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException
from rest_framework import status


from Auth_and_Permission.models import UserModel


class UserAuthentication(BaseAuthentication):
    # 认证方法 认证成功会返回一个元祖，包含用户 和 令牌（token）
    def authenticate(self, request):
        try:
            token = request.query_params.get('token')

            user_id = cache.get(token)

            user = UserModel.objects.get(pk=user_id)
        except Exception as e:
            print(e)
            raise APIException(detail='请先登录好吧', code=status.HTTP_400_BAD_REQUEST)


        return user, token
