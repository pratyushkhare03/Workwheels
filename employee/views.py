from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Employee, EmployeeData
from driver.models import Driver, DriverData
import datetime as dt

# Create your views here.

@login_required
def home(request):
    """
    Employee dashboard - handles both displaying ride requests and shift details form
    """
    date = dt.date.today()
    user = get_object_or_404(User, username=request.user.username)
    
    # Handle shift details form submission
    if request.method == 'POST':
        department = request.POST.get('department', '').strip()
        shift_start = request.POST.get('shift_start', '').strip()
        shift_end = request.POST.get('shift_end', '').strip()
        pickup_location = request.POST.get('pickup_location', '').strip()
        drop_location = request.POST.get('drop_location', '').strip()
        
        # Validation
        if not all([department, shift_start, shift_end, pickup_location, drop_location]):
            messages.error(request, "All fields are required.")
            return redirect('/employee')
        
        try:
            # Get or create employee record
            employee_obj, created = Employee.objects.get_or_create(
                username=user,
                defaults={
                    'department': department,
                    'shift_start': shift_start,
                    'shift_end': shift_end,
                    'pickup_location': pickup_location,
                    'drop_location': drop_location
                }
            )
            
            if created:
                messages.success(request, "Shift details saved successfully!")
            else:
                # Update existing employee record
                employee_obj.department = department
                employee_obj.shift_start = shift_start
                employee_obj.shift_end = shift_end
                employee_obj.pickup_location = pickup_location
                employee_obj.drop_location = drop_location
                employee_obj.save()
                
                # Create history record
                EmployeeData.objects.create(
                    employee=employee_obj,
                    department=department,
                    shift_start=shift_start,
                    shift_end=shift_end,
                    pickup_location=pickup_location,
                    drop_location=drop_location
                )
                
                messages.success(request, "Shift details updated successfully!")
            
            return redirect('/employee')
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('/employee')
    
    # GET request - Display dashboard
    try:
        employee = Employee.objects.get(username=user)
        pickup_location = employee.pickup_location
        drop_location = employee.drop_location
    except Employee.DoesNotExist:
        employee = None
        pickup_location = None
        drop_location = None
    
    # Get last repeated employee data
    rep_employee = None
    rep_pickup_location = None
    rep_drop_location = None
    
    if employee:
        rep_employee = EmployeeData.objects.filter(employee=employee).last()
        if rep_employee:
            rep_pickup_location = rep_employee.pickup_location
            rep_drop_location = rep_employee.drop_location
    
    # Get all drivers and their data
    drivers = Driver.objects.filter(accept_status=True)
    repeated_drivers = DriverData.objects.filter(accept_status=True)
    
    # Prepare driver data for accepted rides
    driver_rides = []
    for driver in drivers:
        driver_rides.append({
            'driver': driver,
            'car_model': driver.carModel,
            'car_numberplate': driver.carNumberPlate,
            'car_capacity': driver.carCapacity,
            'trip_cost': driver.tripCost,
            'pick_uptime': driver.pick_up_time,
            'pickup_location': pickup_location,
            'drop_location': drop_location,
            'status': 'accepted'
        })
    
    # Prepare repeated driver data
    repeated_rides = []
    for rep_driver in repeated_drivers:
        repeated_rides.append({
            'driver': rep_driver,
            'car_model': rep_driver.carModel,
            'car_numberplate': rep_driver.carNumberPlate,
            'car_capacity': rep_driver.carCapacity,
            'trip_cost': rep_driver.tripCost,
            'pick_uptime': rep_driver.pick_up_time,
            'pickup_location': rep_pickup_location,
            'drop_location': rep_drop_location,
            'status': 'accepted'
        })
    
    context = {
        'date': date,
        'employee': employee,
        'pickup_location': pickup_location,
        'drop_location': drop_location,
        'rep_pickup_location': rep_pickup_location,
        'rep_drop_location': rep_drop_location,
        'driver_rides': driver_rides,
        'repeated_rides': repeated_rides,
        'drivers': drivers,
        'repeated_drivers': repeated_drivers,
    }
    
    return render(request, 'employee/home.html', context)


# Remove the old employee() function since it's now combined with home()