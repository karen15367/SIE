from django.urls import path
from . import views

urlpatterns = [
    path('', views.e1),
    path('encuesta1/', views.e1, name='e1'),
    path('encuesta2/', views.e2, name='e2'),
    path('encuesta3/', views.e3, name='e3'),
    path('encuesta4/', views.e4, name='e4'),
    path('encuesta5/', views.e5, name='e5'),
    path('encuesta6/', views.e6, name='e6'),
    path('encuesta7/', views.e7, name='e7'),
    path('encuesta8/', views.e8, name='e8'),
    path('encuesta9/', views.e9, name='e9'),
    path('encuesta10/', views.e10, name='e10'),
    path('encuesta11/', views.e11, name='e11'),
    path('encuesta12/', views.e12, name='e12'),
    path('encuesta/finalizada/', views.encuesta_finalizada, name='encuesta_finalizada'),
    path('acuse/pdf/', views.generar_acuse_pdf, name='acuse_pdf'),
]