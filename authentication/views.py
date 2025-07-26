from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'sitemaster.html')
def register(request):
    return render(request, 'register.html')
def hr(request):
    return render(request, 'hr/register.html')
def employee(request):
    return render(request, 'employee/register.html')