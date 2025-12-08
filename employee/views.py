from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import Employee
from .models import EmployeeData
from driver.models import Driver
from driver.models import DriverData
import datetime as dt
# Create your views here.
@login_required


def home(request):
       date = dt.date.today()
       user = get_object_or_404(User, username=request.user.username)
       employee = Employee.objects.get(username=user)
       
       pickup_location=employee.pickup_location
       drop_location=employee.drop_location
       rep_employee = EmployeeData.objects.filter(employee=employee).last()
       rep_pickup_location=None
       rep_drop_location=None
       if rep_employee:
        rep_pickup_location=rep_employee.pickup_location
        rep_drop_location=rep_employee.drop_location
       
       drivers=Driver.objects.all()
       repeated_drivers=DriverData.objects.all()
        
       rep_car_model=None
       rep_car_numberplate=None
       rep_car_capacity=None
       rep_trip_cost=None
       rep_pick_uptime=None
       
           

       for driver in drivers:
              if driver.accept_status==True:
              # drivername=driver.username
               car_model=driver.carModel
               car_numberplate=driver.carNumberPlate
               car_capacity=driver.carCapacity
               trip_cost=driver.tripCost
               pick_uptime=driver.pick_up_time
              else:
                    car_model=""
                    car_numberplate=""
                    car_capacity=""
                    trip_cost=""
                    pick_uptime=""

       for repeat_driver in repeated_drivers:
            if repeat_driver.accept_status==True:  
              # rep_drivername=repeat_driver.username
              rep_car_model=repeat_driver.carModel
              rep_car_numberplate=repeat_driver.carNumberPlate
              rep_car_capacity=repeat_driver.carCapacity
              rep_trip_cost=repeat_driver.tripCost
              rep_pick_uptime=repeat_driver.pick_up_time
       

       return render(request,'employee/home.html',{'date':date,'car_model':car_model,'car_numberplate':car_numberplate
                     ,'car_capacity':car_capacity,'trip_cost':trip_cost,'pick_uptime':pick_uptime,
                     'rep_car_model':rep_car_model,'rep_car_numberplate':rep_car_numberplate,'rep_car_capacity':rep_car_capacity,
                     'rep_trip_cost':rep_trip_cost,'rep_pick_uptime':rep_pick_uptime,'drivers':drivers,'repeated_drivers':repeated_drivers,
                     'pickup_location':pickup_location,'rep_pickup_location':rep_pickup_location,'drop_location':drop_location,'rep_drop_location':rep_drop_location})


def employee(request):

      user = User.objects.get(username=request.user.username)
      if request.method == 'POST':
             department = request.POST['department']
             shift_start = request.POST['shift_start']
             shift_end = request.POST['shift_end']
             pickup_location = request.POST['pickup_location']
             try:
                    user = get_object_or_404(User, username=request.user.username)
                    employee_obj, created=Employee.objects.get_or_create(
                           username=user,
                           defaults={
                                  'department':department,
                                  'shift_start':shift_start,
                                  'shift_end':shift_end,
                                  'pickup_location':pickup_location
                           }
                    )

                    if not created:
                           EmployeeData.objects.create(
                                  employee=employee_obj,
                                  department=department,
                                  shift_start=shift_start,
                                  shift_end=shift_end,
                                  pickup_location=pickup_location
                           )

                    return redirect('home/')   
             except Exception as e:
                    print("Error:", e)
                    return render(request, 'employee/content.html', {'error': str(e)})
       #      #  pick_up_time = request.POST['pick_up_time']
       #      #  drop_time = request.POST['drop_time']
       #       Employee.objects.create(username=user, department=department, shift_start=shift_start,
       #                                            shift_end=shift_end,pickup_location=pickup_location)
         
       #      #  user = User.objects.filter(is_staff=True)
       #      # usernm = User.username
       #          # driver.save() 
       #       redirect('home/')
      return render(request, 'employee/content.html')



  #

