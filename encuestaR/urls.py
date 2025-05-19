from django.urls import path
from . import views

urlpatterns = [
    path('', views.viewEncuesta),
    path('E1/', views.viewE1),
    path('E2/', views.viewE2),
    # path('A3/', views.viewA3),
    path('E4/', views.viewE4, name='E4'),
    path('exportarE1/', views.exportarE1, name='exportarE1'),
    path('exportarE2/', views.exportarE2, name='exportarE2'),
    path('E5/', views.viewE5, name='E5'),
    path('exportarE5/', views.exportarE5, name='exportarE5'),
    path('exportarE4/', views.exportarE4, name='exportarE4'),


]
