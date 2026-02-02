from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.home, name='employee_home'),
      path('send-request/', views.send_ride_request, name='send_ride_request'),
    path('cancel-request/<int:request_id>/', views.cancel_ride_request, name='cancel_ride_request'),
]