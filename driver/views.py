from django.shortcuts import render

# Create your views here.
def driver(request):
   return render(request, 'driver/content.html')
def home(request):
   return render(request, 'driver/')