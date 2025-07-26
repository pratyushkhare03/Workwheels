from django.urls import path,include
from . import views

urlpatterns = [
    path('driver/',views.hr,name="hr"),
]