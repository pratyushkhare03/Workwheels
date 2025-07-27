from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.driver,name="hr"),
    path('home',views.driverhome,name="driverhome")
]