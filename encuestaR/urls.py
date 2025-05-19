from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewEncuesta),
    path('E1/', views.viewE1),
    #path('A2/', views.viewA2),
    #path('A3/', views.viewA3),
    #path('A4/', views.viewA4),
]
