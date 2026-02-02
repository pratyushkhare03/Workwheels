from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Employee, EmployeeData, RideRequest
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
        
        # Try to get employee data
        try:
            employee = Employee.objects.get(username=user)
            pickup_location = employee.pickup_location or "Not set"
            drop_location = employee.drop_location or "Not set"
        except Employee.DoesNotExist:
            print(f"No Employee record found for user: {user.username}")
        
        # Get all available drivers
        available_drivers = []
        try:
            drivers = Driver.objects.all()
            for driver in drivers:
                # Check if employee already has a pending request with this driver
                has_pending_request = False
                if employee:
                    has_pending_request = RideRequest.objects.filter(
                        employee=employee,
                        driver=driver,
                        status='pending'
                    ).exists()
                
                available_drivers.append({
                    'id': driver.id,
                    'driver_name': driver.username.username,
                    'car_model': driver.carModel or "N/A",
                    'car_numberplate': driver.carNumberPlate or "N/A",
                    'car_capacity': driver.carCapacity or "N/A",
                    'trip_cost': driver.tripCost or "0",
                    'pick_up_time': driver.pick_up_time or "Not specified",
                    'has_pending_request': has_pending_request,
                })
        except Exception as e:
            print(f"Error getting Driver data: {str(e)}")
        
        # Get employee's ride requests with status
        ride_requests = []
        try:
            if employee:
                requests = RideRequest.objects.filter(employee=employee).order_by('-created_at')
                for req in requests:
                    ride_requests.append({
                        'id': req.id,
                        'driver_name': req.driver.username.username if req.driver else "N/A",
                        'car_model': req.driver.carModel if req.driver else "N/A",
                        'car_numberplate': req.driver.carNumberPlate if req.driver else "N/A",
                        'car_capacity': req.driver.carCapacity if req.driver else "N/A",
                        'trip_cost': req.driver.tripCost if req.driver else "0",
                        'pickup_location': req.pickup_location,
                        'drop_location': req.drop_location,
                        'pickup_time': req.pickup_time,
                        'pickup_date': req.pickup_date,
                        'status': req.status,
                        'created_at': req.created_at,
                    })
        except Exception as e:
            print(f"Error getting RideRequest data: {str(e)}")
        
        context = {
            'date': date,
            'employee': employee,
            'pickup_location': pickup_location,
            'drop_location': drop_location,
            'available_drivers': available_drivers,
            'ride_requests': ride_requests,
        }
        
        return render(request, 'employee/home.html', context)
        
    except Exception as e:
        # Catch any unexpected errors
        print(f"Unexpected error in employee home view: {str(e)}")
        import traceback
        traceback.print_exc()
        messages.error(request, "An unexpected error occurred. Please contact support.")
        return redirect('/')


@login_required
def send_ride_request(request, driver_id):
    """
    Handle employee sending a ride request to a driver
    """
    if request.method == 'POST':
        try:
            user = request.user
            employee = get_object_or_404(Employee, username=user)
            driver = get_object_or_404(Driver, id=driver_id)
            
            # Check if already has pending request with this driver
            existing_request = RideRequest.objects.filter(
                employee=employee,
                driver=driver,
                status='pending'
            ).exists()
            
            if existing_request:
                messages.warning(request, "You already have a pending request with this driver.")
                return redirect('/employee')
            
            # Get form data
            pickup_location = request.POST.get('pickup_location', employee.pickup_location)
            drop_location = request.POST.get('drop_location', employee.drop_location)
            pickup_time = request.POST.get('pickup_time', employee.shift_start)
            pickup_date = request.POST.get('pickup_date', dt.date.today())
            notes = request.POST.get('notes', '')
            
            # Create ride request
            RideRequest.objects.create(
                employee=employee,
                driver=driver,
                pickup_location=pickup_location,
                drop_location=drop_location,
                pickup_time=pickup_time,
                pickup_date=pickup_date,
                notes=notes,
                status='pending'
            )
            
            messages.success(request, f"Ride request sent to {driver.username.username} successfully!")
            return redirect('/employee')
            
        except Exception as e:
            print(f"Error sending ride request: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, "Failed to send ride request. Please try again.")
            return redirect('/employee')
    
    return redirect('/employee')


@login_required
def cancel_ride_request(request, request_id):
    """
    Handle employee canceling a pending ride request
    """
    if request.method == 'POST':
        try:
            user = request.user
            employee = get_object_or_404(Employee, username=user)
            ride_request = get_object_or_404(RideRequest, id=request_id, employee=employee)
            
            if ride_request.status == 'pending':
                ride_request.delete()
                messages.success(request, "Ride request canceled successfully!")
            else:
                messages.warning(request, f"Cannot cancel a {ride_request.status} request.")
            
            return redirect('/employee')
            
        except Exception as e:
            print(f"Error canceling ride request: {str(e)}")
            messages.error(request, "Failed to cancel ride request.")
            return redirect('/employee')
    
    return redirect('/employee')