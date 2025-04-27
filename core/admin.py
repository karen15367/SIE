from django.contrib import admin
from .models import (
    Egresado,
    Administrador,
    Encuesta,
    EncuestaS1,
    EncuestaS2,
    EncuestaS3,
    EncuestaS3Empresa,
    EncuestaS4,
    EncuestaS5,
    AnexoS1,
    AnexoS2,
    AnexoS3,
    AnexoS4,
    OpcionesSeleccionMultiple,
    RespuestaSeleccionMultiple,
    Notificacion
)

# Registrar todos los modelos
admin.site.register(Egresado)
admin.site.register(Administrador)
admin.site.register(Encuesta)
admin.site.register(EncuestaS1)
admin.site.register(EncuestaS2)
admin.site.register(EncuestaS3)
admin.site.register(EncuestaS3Empresa)
admin.site.register(EncuestaS4)
admin.site.register(EncuestaS5)
admin.site.register(AnexoS1)
admin.site.register(AnexoS2)
admin.site.register(AnexoS3)
admin.site.register(AnexoS4)
admin.site.register(OpcionesSeleccionMultiple)
admin.site.register(RespuestaSeleccionMultiple)
admin.site.register(Notificacion)
