from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Driver, DriverData
from employee.models import Employee, EmployeeData, RideRequest
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
        
        # Get pending ride requests for this driver
        pending_requests = []
        accepted_requests = []
        try:
            if driver:
                # Pending requests
                pending = RideRequest.objects.filter(driver=driver, status='pending').order_by('-created_at')
                for req in pending:
                    pending_requests.append({
                        'id': req.id,
                        'employee_name': req.employee.username.username,
                        'department': req.employee.department,
                        'pickup_location': req.pickup_location,
                        'drop_location': req.drop_location,
                        'pickup_time': req.pickup_time,
                        'pickup_date': req.pickup_date,
                        'notes': req.notes or "",
                        'created_at': req.created_at,
                        'trip_cost': driver.tripCost,
                    })
                
                # Accepted requests
                accepted = RideRequest.objects.filter(driver=driver, status='accepted').order_by('-created_at')
                for req in accepted:
                    accepted_requests.append({
                        'id': req.id,
                        'employee_name': req.employee.username.username,
                        'department': req.employee.department,
                        'pickup_location': req.pickup_location,
                        'drop_location': req.drop_location,
                        'pickup_time': req.pickup_time,
                        'pickup_date': req.pickup_date,
                        'notes': req.notes or "",
                        'trip_cost': driver.tripCost,
                    })
        except Exception as e:
            print(f"Error getting RideRequest data: {str(e)}")
            import traceback
            traceback.print_exc()
        
        context = {
            'date': date,
            'driver': driver,
            'pending_requests': pending_requests,
            'accepted_requests': accepted_requests,
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
def accept_request(request, request_id):
    """
    Handle driver accepting a ride request
    """
    if request.method == 'POST':
        try:
            user = request.user
            driver = get_object_or_404(Driver, username=user)
            ride_request = get_object_or_404(RideRequest, id=request_id, driver=driver)
            
            if ride_request.status == 'pending':
                ride_request.status = 'accepted'
                ride_request.save()
                
                # Update driver's accept status
                driver.accept_status = True
                driver.assigned_employee = ride_request.employee
                driver.save()
                
                messages.success(request, f"Ride request from {ride_request.employee.username.username} accepted successfully!")
            else:
                messages.warning(request, "This request has already been processed.")
            
            return redirect('/driver')
            
        except Exception as e:
            print(f"Error accepting request: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, "Failed to accept request. Please try again.")
            return redirect('/driver')
    
    return redirect('/driver')


@login_required
def reject_request(request, request_id):
    """
    Handle driver rejecting a ride request
    """
    if request.method == 'POST':
        try:
            user = request.user
            driver = get_object_or_404(Driver, username=user)
            ride_request = get_object_or_404(RideRequest, id=request_id, driver=driver)
            
            if ride_request.status == 'pending':
                ride_request.status = 'rejected'
                ride_request.save()
                
                messages.success(request, f"Ride request from {ride_request.employee.username.username} rejected.")
            else:
                messages.warning(request, "This request has already been processed.")
            
            return redirect('/driver')
            
        except Exception as e:
            print(f"Error rejecting request: {str(e)}")
            messages.error(request, "Failed to reject request. Please try again.")
            return redirect('/driver')
    
    return redirect('/driver')


@login_required
def complete_ride(request, request_id):
    """
    Handle driver completing a ride
    """
    if request.method == 'POST':
        try:
            user = request.user
            driver = get_object_or_404(Driver, username=user)
            ride_request = get_object_or_404(RideRequest, id=request_id, driver=driver)
            
            if ride_request.status == 'accepted':
                ride_request.status = 'completed'
                ride_request.save()
                
                # Reset driver status if no other active rides
                active_rides = RideRequest.objects.filter(driver=driver, status='accepted').exists()
                if not active_rides:
                    driver.accept_status = False
                    driver.assigned_employee = None
                    driver.save()
                
                messages.success(request, "Ride completed successfully!")
            else:
                messages.warning(request, "Invalid ride status.")
            
            return redirect('/driver')
            
        except Exception as e:
            print(f"Error completing ride: {str(e)}")
            messages.error(request, "Failed to complete ride.")
            return redirect('/driver')
    
    return redirect('/driver')