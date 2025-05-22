#signinAdmin/urls.py
from django.urls import path
from . import views
from django.urls import include

app_name = 'signinAdmin'

urlpatterns = [
    path('', views.vistaSignUpAdmin, name='admin_signup'),
    path('verify/', views.verify, name='verify'),
    path('confirmar/<str:token>/', views.confirm_email, name='confirm_email'),
    path('verificacion-pendiente/', views.vistaVerificacionPendiente, name='verificacion_pendiente'),
]
