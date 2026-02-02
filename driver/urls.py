from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.home, name='driver_home'),
    path('accept/<int:request_id>/', views.accept_request, name='accept_req'),
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('complete/<int:request_id>/', views.complete_ride, name='complete_ride'),
]