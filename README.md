# Django-restframework
APIView

### 1.配置环境

创建虚拟环境

```python
# 先保证本地环境中有创建虚拟环境的包
pip install virtualenv
# 到项目文件夹中创建该项目所需要的环境
virtualenv 虚拟环境名字
# 激活环境（Linux下）
source env/bin/activate
# windows下
环境名字\Scripts\activate
# 要退出虚拟环境直接deactivate
```

### 2.创建Django项目

```python
# 先创建好一个Django项目
django-admin.py startproject 项目名
# 然后在该项目创建虚拟环境，安装相应的包
pip install django
pip install djangorestframework
# 在该项目文件中创建app
django-admin.py startapp app名字
# 然后在setting.py 中添加配置
INSTALLED_APPS = [
    ...
    'rest_framework',
    'app名字.apps.AppConfig',
]
# 去app下面的__init__.py 中添加
import pymysql
pymysql.install_as_MySQLdb()
# 然后修改setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangoDay',
        'USER':'root',
        'PASSWORD':'961008',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

```

### 3.创建model

 例如创建一个用户类

```python
from django.db import models

# Create your models here.

#用户模型
class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
```

创建完之后可以迁移数据库了

```python
# 迁移数据库
python manage.py makemigrations
# 在数据库中创建表结构
python manage.py migrate

# 如果有多个app，要分开迁移，在迁移指令后面加上相应的app名字即可

```

#### (1)出现问题

迁移时出现的问题,  TypeError: init() missing 1 required positional argument: ‘on_delete’

当执行 python [manage.py](http://manage.py/) makemigrations 出现错误：TypeError: **init**() missing 1 required positional argument: ‘on_delete’

#### (2)解决方案

```python
# 定义外键的时候需要加上 on_delete=;
# 比如，用户和博客类之间的关联
author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
```

#### (3)问题原因

django 升级到2.0之后,表与表之间关联的时候,必须要写on_delete参数,否则会报异常:
TypeError: init() missing 1 required positional argument: ‘on_delete’

on_delete各个参数的含义如下：

```python
on_delete=None,               # 删除关联表中的数据时,当前表与其关联的field的行为
	on_delete=models.CASCADE,     # 删除关联数据,与之关联也删除
	on_delete=models.DO_NOTHING,  # 删除关联数据,什么也不做
	on_delete=models.PROTECT,     # 删除关联数据,引发错误ProtectedError
	# models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
	on_delete=models.SET_NULL,    # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
	# models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
	on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
	on_delete=models.SET,         # 删除关联数据,
	 a. 与之关联的值设置为指定值,设置：models.SET(值)
	 b. 与之关联的值设置为可执行对象的返回值,设置：models.SET(可执行对象)
————————————————
版权声明：本文为CSDN博主「KreaWu」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/KreaWu/article/details/89400647
```

**由于多对多(ManyToManyField)没有 on_delete 参数,所以以上只针对外键(ForeignKey)和一对一(OneToOneField)**

### 4.序列化器

运用ModelSerializer

```python
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
```

### 5.编写视图

```python
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
```

### 6.设置路由

#### (1)工程下的路由

```python
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^app/', include('app.urls')),

]
```

#### (2)app下的路由

```python
from django.conf.urls import url

from app import views

urlpatterns =[
    url(r'^users/', views.UserAPI.as_view()),
    url(r'^blogs/', views.BlogsAPIView.as_view())
]
```

### 7.运行

```python
python manage.py runserver
```

