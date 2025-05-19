from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewEncuesta),
    path('E1/', views.viewE1),
    path('E2/', views.viewE2),
    path('E3/', views.viewE3),
    # path('A4/', views.viewA4),
    path('exportarE1/', views.exportarE1, name='exportarE1'),
    path('exportarE2/', views.exportarE2, name='exportarE2'),

]
