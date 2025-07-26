from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    # path('driver/',views.driver,name="driver"),
    # path('hr/',views.hr,name="hr"),
    # path('employee/',views.employee,name="employee"),
]