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
    try:
        date = dt.date.today()
        user = request.user
        
        # Handle shift details form submission (from modal)
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
                
                if not created:
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
                else:
                    messages.success(request, "Shift details saved successfully!")
                
                return redirect('/employee')
                
            except Exception as e:
                print(f"Error saving shift details: {str(e)}")
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('/employee')
        
        # GET request - Display dashboard
        # Initialize default values
        employee = None
        pickup_location = "Not set"
        drop_location = "Not set"
        rep_pickup_location = "Not set"
        rep_drop_location = "Not set"
        
        # Try to get employee data
        try:
            employee = Employee.objects.get(username=user)
            pickup_location = employee.pickup_location or "Not set"
            drop_location = employee.drop_location or "Not set"
        except Employee.DoesNotExist:
            print(f"No Employee record found for user: {user.username}")
        
        # Get last repeated employee data
        rep_employee = None
        if employee:
            try:
                rep_employee = EmployeeData.objects.filter(employee=employee).order_by('-id').first()
                if rep_employee:
                    rep_pickup_location = rep_employee.pickup_location or "Not set"
                    rep_drop_location = rep_employee.drop_location or "Not set"
            except Exception as e:
                print(f"Error getting EmployeeData: {str(e)}")
        
        # Get accepted drivers
        driver_rides = []
        try:
            drivers = Driver.objects.filter(accept_status=True)
            for driver in drivers:
                driver_rides.append({
                    'car_model': driver.carModel or "N/A",
                    'car_numberplate': driver.carNumberPlate or "N/A",
                    'car_capacity': driver.carCapacity or "N/A",
                    'trip_cost': driver.tripCost or "0",
                    'pick_uptime': driver.pick_up_time or "Not specified",
                    'pickup_location': pickup_location,
                    'drop_location': drop_location,
                })
        except Exception as e:
            print(f"Error getting Driver data: {str(e)}")
        
        # Get repeated accepted drivers
        repeated_rides = []
        try:
            repeated_drivers = DriverData.objects.filter(accept_status=True)
            for rep_driver in repeated_drivers:
                repeated_rides.append({
                    'car_model': rep_driver.carModel or "N/A",
                    'car_numberplate': rep_driver.carNumberPlate or "N/A",
                    'car_capacity': rep_driver.carCapacity or "N/A",
                    'trip_cost': rep_driver.tripCost or "0",
                    'pick_uptime': rep_driver.pick_up_time or "Not specified",
                    'pickup_location': rep_pickup_location,
                    'drop_location': rep_drop_location,
                })
        except Exception as e:
            print(f"Error getting DriverData: {str(e)}")
        
        context = {
            'date': date,
            'employee': employee,
            'pickup_location': pickup_location,
            'drop_location': drop_location,
            'rep_pickup_location': rep_pickup_location,
            'rep_drop_location': rep_drop_location,
            'driver_rides': driver_rides,
            'repeated_rides': repeated_rides,
        }
        
        return render(request, 'employee/home.html', context)
        
    except Exception as e:
        # Catch any unexpected errors
        print(f"Unexpected error in employee home view: {str(e)}")
        import traceback
        traceback.print_exc()
        messages.error(request, "An unexpected error occurred. Please contact support.")
        return redirect('/')