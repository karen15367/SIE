from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewAnexos),
    path('A1/', views.viewA1),
    path('A2/', views.viewA2),
    path('A3/', views.viewA3),
]
