from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Driver, DriverData
from employee.models import Employee, EmployeeData
import datetime as dt

# Create your views here.

@login_required
def home(request):
    """
    Driver dashboard - handles both displaying ride requests and car details form
    """
    try:
        date = dt.date.today()
        user = request.user
        
        # Handle car details form submission (from modal)
        if request.method == 'POST':
            car_model = request.POST.get('carModel', '').strip()
            car_numberplate = request.POST.get('carNumberPlate', '').strip()
            car_capacity = request.POST.get('carCapacity', '').strip()
            pick_up_time = request.POST.get('pick_up_time', '').strip()
            drop_time = request.POST.get('drop_time', '').strip()
            trip_cost = request.POST.get('tripcost', '').strip()
            
            # Validation
            if not all([car_model, car_numberplate, car_capacity, pick_up_time, drop_time, trip_cost]):
                messages.error(request, "All fields are required.")
                return redirect('/driver')
            
            try:
                # Get or create driver record
                driver_obj, created = Driver.objects.get_or_create(
                    username=user,
                    defaults={
                        'carModel': car_model,
                        'carNumberPlate': car_numberplate,
                        'carCapacity': car_capacity,
                        'pick_up_time': pick_up_time,
                        'drop_time': drop_time,
                        'tripCost': trip_cost,
                        'accept_status': False
                    }
                )
                
                if not created:
                    # Update existing driver record
                    driver_obj.carModel = car_model
                    driver_obj.carNumberPlate = car_numberplate
                    driver_obj.carCapacity = car_capacity
                    driver_obj.pick_up_time = pick_up_time
                    driver_obj.drop_time = drop_time
                    driver_obj.tripCost = trip_cost
                    driver_obj.save()
                    
                    # Create history record
                    DriverData.objects.create(
                        driver=driver_obj,
                        carModel=car_model,
                        carNumberPlate=car_numberplate,
                        carCapacity=car_capacity,
                        pick_up_time=pick_up_time,
                        drop_time=drop_time,
                        tripCost=trip_cost,
                        accept_status=False
                    )
                    
                    messages.success(request, "Car details updated successfully!")
                else:
                    messages.success(request, "Car details saved successfully!")
                
                return redirect('/driver')
                
            except Exception as e:
                print(f"Error saving car details: {str(e)}")
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('/driver')
        
        # GET request - Display dashboard
        # Initialize default values
        driver = None
        
        # Try to get driver data
        try:
            driver = Driver.objects.get(username=user)
        except Driver.DoesNotExist:
            print(f"No Driver record found for user: {user.username}")
        
        # Get all employees with ride requests
        employee_requests = []
        try:
            employees = Employee.objects.all()
            for employee in employees:
                employee_requests.append({
                    'employeename': employee.username.username,
                    'pickup_location': employee.pickup_location or "Not specified",
                    'drop_location': employee.drop_location or "Not specified",
                    'pickup_time': employee.shift_start or "Not specified",
                    'trip_cost': driver.tripCost if driver else "0",
                })
        except Exception as e:
            print(f"Error getting Employee data: {str(e)}")
        
        # Get repeated employee requests
        repeated_requests = []
        try:
            rep_employees = EmployeeData.objects.all()
            for rep_employee in rep_employees:
                repeated_requests.append({
                    'rep_employeename': rep_employee.employee.username.username,
                    'rep_pickup_location': rep_employee.pickup_location or "Not specified",
                    'rep_drop_location': rep_employee.drop_location or "Not specified",
                    'rep_pickup_time': rep_employee.shift_start or "Not specified",
                    'rep_trip_cost': driver.tripCost if driver else "0",
                })
        except Exception as e:
            print(f"Error getting EmployeeData: {str(e)}")
        
        context = {
            'date': date,
            'driver': driver,
            'employees': employee_requests,
            'rep_employees': repeated_requests,
            'rep_driver': driver,  # For template compatibility
            'employeename': employee_requests[0]['employeename'] if employee_requests else None,
            'pickup_location': employee_requests[0]['pickup_location'] if employee_requests else None,
            'drop_location': employee_requests[0]['drop_location'] if employee_requests else None,
            'pickup_time': employee_requests[0]['pickup_time'] if employee_requests else None,
            'trip_cost': employee_requests[0]['trip_cost'] if employee_requests else None,
        }
        
        return render(request, 'driver/home.html', context)
        
    except Exception as e:
        # Catch any unexpected errors
        print(f"Unexpected error in driver home view: {str(e)}")
        import traceback
        traceback.print_exc()
        messages.error(request, "An unexpected error occurred. Please contact support.")
        return redirect('/')


@login_required
def accept_request(request, driver_id):
    """
    Handle driver accepting a ride request
    """
    if request.method == 'POST':
        try:
            driver = get_object_or_404(Driver, id=driver_id)
            driver.accept_status = True
            driver.save()
            
            messages.success(request, "Ride request accepted successfully!")
            return redirect('/driver')
            
        except Exception as e:
            print(f"Error accepting request: {str(e)}")
            messages.error(request, "Failed to accept request. Please try again.")
            return redirect('/driver')
    
    return redirect('/driver')