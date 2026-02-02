from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255, default="Unknown")
   
    def __str__(self):
        return f"{self.username.username} - {self.department}"
    

class EmployeeData(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='data_entries')
    department = models.CharField(max_length=100)
    shift_start = models.TimeField()
    shift_end = models.TimeField()
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255, default="Unknown")
    
    def __str__(self):
        return f"{self.employee.username.username} - {self.department}"


class RideRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ride_requests')
    driver = models.ForeignKey('driver.Driver', on_delete=models.CASCADE, related_name='ride_requests', null=True, blank=True)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    pickup_time = models.TimeField()
    pickup_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['employee', 'driver', 'status']  # Prevent multiple pending requests to same driver
    
    def __str__(self):
        return f"{self.employee.username.username} - {self.status}"