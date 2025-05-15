from django.urls import path
from . import views
from django.urls import include

app_name = 'signinAdmin'

urlpatterns = [
    # Rutas existentes
    path('', views.vistaSignUpAdmin, name='admin_signup'),
]
