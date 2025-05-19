#importador/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('resumen/', views.resumen_importaciones, name='resumen_importaciones'),
    path('importar-encuesta/', views.procesar_excel_encuesta, name='importar_encuesta'),
    path('importar-anexo/', views.procesar_excel_anexo, name='importar_anexo'),

]