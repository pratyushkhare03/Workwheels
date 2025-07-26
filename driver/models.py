from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class driver(models.Model):
    username=models.OneToOneField(User, on_delete=models.CASCADE)
    carModel=models.CharField(max_length=50)
    carNumberPlate=models.CharField(max_length=50)
    carCapacity=models.CharField(max_length=50)
    tripCost=models.CharField(max_length=50)
    pick_up_time=models.TimeField()
    drop_time=models.TimeField()
    
    def str(self):
        return self.username+""+self.role+""