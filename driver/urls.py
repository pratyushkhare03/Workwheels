from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.driver,name="hr"),
    path('home',views.driverhome,name="driverhome"),
    path('accept/<int:driver_id>/',views.accept_req,name="accept_req")
]