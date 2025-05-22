from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewEncuesta),
    path('E1/', views.viewE1),
    path('E2/', views.viewE2),
    # path('A3/', views.viewA3),
    path('E4/', views.viewE4, name='E4'),
    path('E3/', views.viewE3),
    # path('A4/', views.viewA4),
    path('exportarE1/', views.exportarE1, name='exportarE1'),
    path('exportarE2/', views.exportarE2, name='exportarE2'),
    path('E5/', views.viewE5, name='E5'),
    path('exportarE5/', views.exportarE5, name='exportarE5'),
    path('exportarE4/', views.exportarE4, name='exportarE4'),
    path('exportarE3/', views.exportarE3, name='exportarE3'),
    path('exportar-encuesta/', views.formulario_export_encuesta, name='formulario_export_encuesta'),
    path('exportar-encuesta-por-carrera/', views.exportar_encuesta_por_carrera, name='exportar_encuesta_por_carrera'),
]
