from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    # path('hr/',views.hr,name="hr"),
    # path('employee/',views.employee,name="employee"),
]