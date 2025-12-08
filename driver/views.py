from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Driver
from employee.models import Employee
from employee.models import EmployeeData
from .models import DriverData
import datetime as dt
# Create your views here.
@login_required

def accept_request(request,employee,rep_employee):
    try:
        driver_user = get_object_or_404(User, username=request.user.username)
        driver = get_object_or_404(Driver, username=driver_user)
        driver.accept_status=True
        driver.assigned_employee = employee 
        driver.save()
        rep_driver_data = DriverData.objects.filter(driver=driver).last()
        if rep_driver_data:
            rep_driver_data.active_status = True
            if rep_employee:
             rep_driver_data.assigned_employee = rep_employee  # if DriverData has this field
             rep_driver_data.save()
    except Exception as e:
        print("Error accepting request: {e}")
        return render(request, 'driver/home.html', {'error': str(e)})

    
    return
def driverhome(request):
   print("Driver Home Called")
   if not request.user.is_authenticated:
        return redirect('login')
   date=dt.date.today()
   driver = get_object_or_404(Driver, username=request.user)
   rep_driver = DriverData.objects.filter(driver=driver).first()
   
   print("Driver ID:", driver.id) 
#    print("Driverdata ID:", rep_driver.id) 
   employees = Employee.objects.all()
   rep_employees = EmployeeData.objects.all()
   for employee in employees:
    # employee = Employee.objects.get(id=count.id)
    employeename=employee.username
    pickup_time=employee.shift_end
    pickup_location=employee.pickup_location
    # trip_cost= trip cost is decided by the driver #TODO
   drop_location=employee.drop_location
   rep_employeename=None
   rep_pickup_time=None
   rep_pickup_location=None
    # trip_cost= trip cost is decided by the driver #TODO
   rep_drop_location=None
   
   for rep_employee in rep_employees:
    # employee = Employee.objects.get(id=count.id)
    # rep_employeename=rep_employee.employeename
    if rep_employee:
     rep_employeename_data = EmployeeData.objects.filter(employee=employee).first()
     if rep_employeename_data:
      rep_employeename=rep_employeename_data.employee.username.username
     rep_pickup_time=rep_employee.shift_end 
     rep_pickup_location=rep_employee.pickup_location
    # trip_cost= trip cost is decided by the driver #TODO
     rep_drop_location=rep_employee.drop_location
    
    
   return render(request, 'driver/home.html',{'employees':employees,'rep_employees':rep_employees,'employeename':employeename,
                                               'rep_employeename':rep_employeename,'pickup_time':pickup_time,'rep_pickup_time':rep_pickup_time,
                                               'pickup_location':pickup_location,'rep_pickup_location':rep_pickup_location,'trip_cost':'TODO',
                                               'rep_trip_cost':'TODO','date':date,'rep_drop_location':rep_drop_location,
                                               'drop_location':drop_location,'rep_driver':rep_driver,'driver':driver})

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
            #   accept_status = get_object_or_404(User, username=request.user.accept_status)

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

@require_POST
def accept_req(request, driver_id):
       print("Driver get page")
       try:
          driver = get_object_or_404(DriverData, id=driver_id)
          driver.accept_status = True
          driver.save()
       except:
          driver = get_object_or_404(Driver, id=driver_id)
          driver.accept_status = True
          driver.save()

       return redirect('/driver/home')


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