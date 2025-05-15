from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='sign_in'),  # Esto conecta directamente a /sign-in/
    path('verify/', views.verify, name='verify'),
    path('confirmar/<str:token>/', views.confirm_email, name='confirm_email'),
    path('verificacion-pendiente/', views.vistaVerificacionPendiente, name='verificacion_pendiente'),
]