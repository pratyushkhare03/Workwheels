from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.employee,name="employee"),
    # path('home/',views.employee,name="employee"),  #TODO
]