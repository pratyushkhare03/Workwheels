from django.urls import path,include
from . import views

urlpatterns = [
     path('', views.home, name='driver_home'),
    path('accept/<int:driver_id>/', views.accept_request, name='accept_req'),
]