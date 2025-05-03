from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import datetime

from core.validators import (
    solo_letras_espacios,
    curp_validator,
    rfc_validator,
    numero_control_validator,
    telefono_validator
)

# ---------------------------
# MODELO Egresado
# ---------------------------
class Egresado(models.Model):
    curp = models.CharField(max_length=18, primary_key=True, validators=[curp_validator])
    nombre = models.CharField(max_length=50, validators=[solo_letras_espacios])
    noControl = models.CharField(max_length=9, unique=True, validators=[numero_control_validator])
    correo = models.EmailField(max_length=50, unique=True, validators=[EmailValidator(message='Ingrese un correo electrónico válido')])
    sexo = models.BooleanField()  # 1=Femenino, 0=Masculino
    fechaNacimiento = models.DateField()
    carrera = models.CharField(max_length=50, validators=[solo_letras_espacios])
    titulado = models.BooleanField()
    fechaEgreso = models.DateField()
    contraseña = models.CharField(max_length=64)
    sesion = models.CharField(max_length=64, blank=True, null=True)

    def clean(self):
        hoy = datetime.date.today()
        if self.fechaNacimiento and self.fechaNacimiento > hoy:
            raise ValidationError({'fechaNacimiento': 'La fecha de nacimiento no puede ser posterior a hoy.'})
        if self.fechaEgreso and self.fechaEgreso > hoy:
            raise ValidationError({'fechaEgreso': 'La fecha de egreso no puede ser posterior a hoy.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({self.curp})"

# ---------------------------
# MODELO Administrador
# ---------------------------
class Administrador(models.Model):
    rfc = models.CharField(max_length=13, primary_key=True, validators=[rfc_validator])
    nombre = models.CharField(max_length=50, validators=[solo_letras_espacios])
    correo = models.EmailField(max_length=50, unique=True, validators=[EmailValidator()])
    contraseña = models.CharField(max_length=64)
    sesion = models.CharField(max_length=64, blank=True, null=True)
    carrera = models.CharField(max_length=50,validators=[solo_letras_espacios],blank=True,null=True,
    help_text="Si está vacío, el administrador tiene acceso a todas las carreras.")

    def __str__(self):
        return self.nombre

# ---------------------------
# MODELO Encuesta
# ---------------------------
class Encuesta(models.Model):
    folioEncuesta = models.BigAutoField(primary_key=True)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()
    curp = models.ForeignKey(Egresado, on_delete=models.CASCADE, to_field='curp')
    lapso = models.CharField(max_length=9)

    def clean(self):
        if self.fechaInicio and self.fechaFin and self.fechaInicio > self.fechaFin:
            raise ValidationError('La fecha de inicio no puede ser posterior a la fecha de fin.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Encuesta {self.folioEncuesta}"

# ---------------------------
# MODELOS de Secciones de Encuesta
# ---------------------------
class EncuestaS1(models.Model):
    folioEncuestaS1 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta1 = models.CharField(max_length=50)
    pregunta2 = models.CharField(max_length=50)
    pregunta3 = models.CharField(max_length=50)
    pregunta4 = models.CharField(max_length=50)

    def __str__(self):
        return f"Sección 1 - Encuesta {self.folioEncuesta}"

class EncuestaS2(models.Model):
    folioEncuestaS2 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta5 = models.CharField(max_length=50)
    pregunta6 = models.CharField(max_length=50)
    pregunta7 = models.CharField(max_length=50)
    pregunta8 = models.CharField(max_length=50)
    pregunta9 = models.CharField(max_length=50)

    def __str__(self):
        return f"Sección 2 - Encuesta {self.folioEncuesta}"

class EncuestaS3(models.Model):
    folioEncuestaS3 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta10 = models.CharField(max_length=50)
    pregunta11 = models.CharField(max_length=50)
    pregunta12 = models.CharField(max_length=50)
    pregunta13 = models.CharField(max_length=50)
    pregunta14 = models.CharField(max_length=50)
    pregunta15 = models.CharField(max_length=50)

    def __str__(self):
        return f"Sección 3 - Encuesta {self.folioEncuesta}"

class EncuestaS3Empresa(models.Model):
    folioEncuestaS3Empresa = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    nombreEmpresa = models.CharField(max_length=50)
    giroEmpresa = models.CharField(max_length=50)
    tamanoEmpresa = models.CharField(max_length=50)
    areaTrabajo = models.CharField(max_length=50)

    def __str__(self):
        return f"Empresa {self.nombreEmpresa} - Encuesta {self.folioEncuesta}"

class EncuestaS4(models.Model):
    folioEncuestaS4 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta16 = models.CharField(max_length=50)
    pregunta17 = models.CharField(max_length=50)
    pregunta18 = models.CharField(max_length=50)
    pregunta19 = models.CharField(max_length=50)
    pregunta20 = models.CharField(max_length=50)

    def __str__(self):
        return f"Sección 4 - Encuesta {self.folioEncuesta}"

class EncuestaS5(models.Model):
    folioEncuestaS5 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta21 = models.CharField(max_length=50)
    pregunta22 = models.CharField(max_length=50)
    pregunta23 = models.CharField(max_length=50)

    def __str__(self):
        return f"Sección 5 - Encuesta {self.folioEncuesta}"

# ---------------------------
# MODELOS de Anexos
# ---------------------------
class AnexoS1(models.Model):
    folioAnexoS1 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta24 = models.CharField(max_length=50)
    pregunta25 = models.CharField(max_length=50)
    pregunta26 = models.CharField(max_length=50)

    def __str__(self):
        return f"Anexo S1 - Encuesta {self.folioEncuesta}"

class AnexoS2(models.Model):
    folioAnexoS2 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta27 = models.CharField(max_length=50)
    pregunta28 = models.CharField(max_length=50)

    def __str__(self):
        return f"Anexo S2 - Encuesta {self.folioEncuesta}"

class AnexoS3(models.Model):
    folioAnexoS3 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta29 = models.CharField(max_length=50)
    pregunta30 = models.CharField(max_length=50)
    pregunta31 = models.CharField(max_length=50)

    def __str__(self):
        return f"Anexo S3 - Encuesta {self.folioEncuesta}"

class AnexoS4(models.Model):
    folioAnexoS4 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta32 = models.CharField(max_length=50)
    pregunta33 = models.CharField(max_length=50)

    def __str__(self):
        return f"Anexo S4 - Encuesta {self.folioEncuesta}"

# ---------------------------
# MODELOS de Selección Múltiple
# ---------------------------
class OpcionesSeleccionMultiple(models.Model):
    idOpcion = models.BigAutoField(primary_key=True)
    codigoPregunta = models.CharField(max_length=5)
    textoOpcion = models.CharField(max_length=50)

    def __str__(self):
        return self.textoOpcion

class RespuestaSeleccionMultiple(models.Model):
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    codigoPregunta = models.CharField(max_length=5)
    idOpcion = models.ForeignKey(OpcionesSeleccionMultiple, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('folioEncuesta', 'codigoPregunta'),)

    def __str__(self):
        return f"Respuesta {self.codigoPregunta} - Encuesta {self.folioEncuesta}"

# ---------------------------
# MODELO Notificacion
# ---------------------------
class Notificacion(models.Model):
    idNotificacion = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

    def clean(self):
        if self.fechaInicio and self.fechaFin and self.fechaInicio > self.fechaFin:
            raise ValidationError('La fecha de inicio no puede ser posterior a la fecha de fin.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
