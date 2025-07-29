
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    username=models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    pickup_location = models.CharField(max_length=255)
   
    
    def str(self):
        return self.username+""+self.role+""
    

class EmployeeData(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='data_entries')
    department = models.CharField(max_length=100)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    pickup_location = models.CharField(max_length=255)
   
    
    def str(self):
        return self.username+""+self.role+""

