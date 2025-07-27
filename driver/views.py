from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Driver
# Create your views here.
def driver(request):
      if request.method == 'POST':
       carModel = request.POST['carModel']
       carNumberPlate = request.POST['carNumberPlate']
       carCapacity = request.POST['carCapacity']
       tripCost = request.POST['tripcost']
       pick_up_time = request.POST['pick_up_time']
       drop_time = request.POST['drop_time']
       username = request.user.username
      #  user = User.objects.filter(is_staff=True)
      #  username = user.username
       Driver.objects.create(username=username,carModel=carModel, carNumberPlate=carNumberPlate,
                                            carCapacity=carCapacity,tripCost=tripCost,pick_up_time=pick_up_time,drop_time=drop_time)
      # driver.save() 
      redirect('home/')


      return render(request, 'driver/content.html')



def driverhome(request):


   return render(request, 'driver/content2.html')