from django.urls import path
from . import views

urlpatterns = [
    path('', views.a1),
    path('a1/', views.a1, name='anexo1'),
    path('a2/', views.a2, name='anexo2'),
    path('a3/', views.a3, name='anexo3'),
    path('a4/', views.a4, name='anexo4'),
    path('a5/', views.a5, name='anexo5'),
    path('a6/', views.a6, name='anexo6'),
    path('a7/', views.a7, name='anexo7'),
    path('a8/', views.a8, name='anexo8'),
    path('a9/', views.a9, name='anexo9'),
    path('a10/', views.a10, name='anexo10'),
    path('a11/', views.a11, name='anexo11'),
    path('a12/', views.a12, name='anexo12'),
]
