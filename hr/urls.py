from django.urls import path,include
from . import views

urlpatterns = [
    path('/hr',views.hr,name="hr"),
]