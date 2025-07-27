
# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class USER(models.Model):
    username=models.OneToOneField(User, on_delete=models.CASCADE)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)
    password2=models.CharField(max_length=50)
    role=models.CharField(max_length=50)
    def _str_(self):
        return self.username+" "+self.role+" "




# from django.db import models
# from django.contrib.auth.models import AbstractUser

# from django.contrib.auth.models import User

# # Create your models here.
# class USER(AbstractUser):
#     username=models.OneToOneField(User, on_delete=models.CASCADE)
#     role=models.CharField(max_length=50)
#     def str(self):
#         return self.username+""+self.role+""