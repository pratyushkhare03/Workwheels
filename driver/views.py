from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Driver
from employee.models import Employee
from employee.models import EmployeeData
from .models import DriverData
import datetime as dt
# Create your views here.
@login_required

def driverhome(request):
   date=dt.date.today()
   employees = Employee.objects.all()
   rep_employees = EmployeeData.objects.all()
   for employee in employees:
    # employee = Employee.objects.get(id=count.id)
    employeename=employee.username
    pickup_time=employee.shift_end
    pickup_location=employee.pickup_location
    # trip_cost= trip cost is decided by the driver #TODO
    # drop_location #TODO

   for rep_employee in rep_employees:
    # employee = Employee.objects.get(id=count.id)
    # rep_employeename=rep_employee.employeename
    rep_employeename_data = EmployeeData.objects.filter(employee=employee).last()
    rep_employeename=rep_employeename_data.employee.username.username
    rep_pickup_time=rep_employee.shift_end
    rep_pickup_location=rep_employee.pickup_location
    # trip_cost= trip cost is decided by the driver #TODO
    # drop_location #TODO
    





    return render(request, 'driver/home.html',{'employees':employees,'rep_employees':rep_employees,'employeename':employeename,
                                               'rep_employeename':rep_employeename,'pickup_time':pickup_time,'rep_pickup_time':rep_pickup_time,
                                               'pickup_location':pickup_location,'rep_pickup_location':rep_pickup_location,'trip_cost':'TODO','drop_location':'TODO',
                                               'rep_trip_cost':'TODO','rep_drop_location':'TODO','date':date})

def driver(request):
       if request.method == 'POST':
        carModel = request.POST['carModel']
        carNumberPlate = request.POST['carNumberPlate']
        carCapacity = request.POST['carCapacity']
        tripCost = request.POST['tripcost']
        pick_up_time = request.POST['pick_up_time']
        drop_time = request.POST['drop_time']
        try:

              # Get logged-in user
              user = get_object_or_404(User, username=request.user.username)

              # Check if Driver exists for this user
              driver_obj, created = Driver.objects.get_or_create(
                  username=user,
                  defaults={
                      'carModel': carModel,
                      'carNumberPlate': carNumberPlate,
                      'carCapacity': carCapacity,
                      'tripCost': tripCost,
                      'pick_up_time': pick_up_time,
                      'drop_time': drop_time
                  }
              )

              # If Driver already existed, save details in DriverData
              if not created:
                  DriverData.objects.create(
                      driver=driver_obj,  # pass object, not ID
                      carModel=carModel,
                      carNumberPlate=carNumberPlate,
                      carCapacity=carCapacity,
                      tripCost=tripCost,
                      pick_up_time=pick_up_time,
                      drop_time=drop_time
                  )
      
              return redirect('/driver/home')
        except Exception as e:
               # Log the error (optional: print or save to log file)
              print("Error:", e)
               # You can pass error message to template if needed
        return render(request, 'driver/content.html', {'error': str(e)})
       return render(request,'driver/content.html')




            # username = request.user.username 
            # user = User.objects.get(username=request.user.username)
            
            # if request.method == 'POST':
            #  carModel = request.POST['carModel']
            #  carNumberPlate = request.POST['carNumberPlate']
            #  carCapacity = request.POST['carCapacity']
            #  tripCost = request.POST['tripcost']
            #  pick_up_time = request.POST['pick_up_time']
            #  drop_time = request.POST['drop_time']
            #  try:
            #       user = User.objects.get(username=request.user.username)
            #       Driver.objects.create(username=user, carModel=carModel, carNumberPlate=carNumberPlate,
            #                                         carCapacity=carCapacity,tripCost=tripCost,pick_up_time=pick_up_time,drop_time=drop_time)
            #  except:
            #         user = Driver.objects.get(username=request.user.username)
            #         DriverData.objects.create(driver=user.id, carModel=carModel, carNumberPlate=carNumberPlate,
            #                                       carCapacity=carCapacity,tripCost=tripCost,pick_up_time=pick_up_time,drop_time=drop_time)
             
            # #  user = User.objects.filter(is_staff=True)
            # # usernm = User.username
            #     # driver.save() 
            # return redirect('/home')