from rest_framework import serializers

from Auth_and_Permission.models import UserModel, Blog


#序列化器
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password')


class BlogSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = ('id', 'title', 'content', 'author')