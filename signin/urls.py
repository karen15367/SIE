from django.urls import path
from  . import views
import include
from django.urls import include

urlpatterns = [
    
    path('', views.signin),
    path('', views.vistaLogin),
    path('verify/', views.verify),
    path("confirmar/<str:token>/", views.confirm_email, name="confirm_email"),
    path('verificacion-pendiente/', views.vistaVerificacionPendiente, name="verificacion_pendiente"),
    
]
