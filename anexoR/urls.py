# urls.py
from django.urls import path
from . import views

app_name = 'anexoR'  # Esto define el namespace para las referencias en las plantillas

urlpatterns = [
    path('', views.viewAnexos, name='index'),
    path('A1/', views.viewA1, name='A1'),  # Agregamos name='A1'
    path('A2/', views.viewA2, name='A2'),  # Agregamos name='A2'
    path('A3/', views.viewA3, name='A3'),  # Agregamos name='A3'
    path('exportarA1/', views.exportarA1, name='exportarA1'),
    path('exportarA2/', views.exportarA2, name='exportarA2'),
    path('exportarA3/', views.exportarA3, name='exportarA3'),
    path('exportarA4/', views.exportarA4, name='exportarA4'),
    path('A4/', views.A4, name='A4'),
    path('exportar-anexo/', views.formulario_export_anexo, name='formulario_export_anexo'),
    path('exportar-anexo-por-carrera/', views.exportar_anexo_por_carrera, name='exportar_anexo_por_carrera'),
]
