from django.db import models

# Create your models here.

#用户模型
class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)



    # 验证密码
    def verify_password(self, password):
        return  self.password == password

class Blog(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()


