from django.shortcuts import render

# Create your views here.
def employee(request):
    return render(request, 'employee/content.html')