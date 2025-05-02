from django.urls import path
from  . import views

urlpatterns = [
    
    path('', views.signin),
    path('verify/', views.verify),
    path('noc/', views.confirm_email),
]
