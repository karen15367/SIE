#index/urls.py
from django.urls import path
from . import views
from django.urls import include
from importador.views import procesar_excel_anexo, procesar_excel_encuesta
from core.models import EstadoEncuestaCarrera


urlpatterns = [
    path('', views.index, name='index'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crear-aviso/', views.crear_aviso, name='crear_aviso'),
    path('editar-aviso/<int:idNotificacion>/',views.editar_aviso, name='editar_aviso'),
    path('vistaSignUpAdmin/', views.vistaSignUpAdmin, name='vistaSignUpAdmin'),

    path('consulta/', views.resultados, name='resultados'),
    path('modUser/', views.modUser, name='modUser'),
    path('newPwd/', views.newPwd, name='newPwd'),
    path('modCampos/', views.modCampos, name='modCampos'),
    path('importar-anexo/', procesar_excel_anexo, name='importar_anexo'),
    path('importar-encuesta/', procesar_excel_encuesta, name='importar_encuesta'),
    path('estado-encuestas/', views.vista_estado_encuestas, name='vista_estado_encuestas'),
    path('encuestaBloqueada/', views.encuesta_bloqueada, name='encuesta_bloqueada'),

]
