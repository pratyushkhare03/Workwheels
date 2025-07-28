from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Employee
# Create your views here.
@login_required
def employee(request):

      user = User.objects.get(username=request.user.username)
      if request.method == 'POST':
             department = request.POST['department']
             shift_start = request.POST['shift_start']
             shift_end = request.POST['shift_end']
             pickup_location = request.POST['pickup_location']
            #  pick_up_time = request.POST['pick_up_time']
            #  drop_time = request.POST['drop_time']
             Employee.objects.create(username=user, department=department, shift_start=shift_start,
                                                  shift_end=shift_end,pickup_location=pickup_location)
         
            #  user = User.objects.filter(is_staff=True)
            # usernm = User.username
                # driver.save() 
             redirect('home/')
      return render(request, 'employee/content.html')