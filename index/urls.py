from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crear-aviso/', views.crear_aviso, name='crear_aviso'),
    path('editar-aviso/<int:idNotificacion>/', views.editar_aviso, name='editar_aviso'),
]