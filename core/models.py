from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import datetime
from django.utils.timezone import now


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
    nombre = models.CharField(max_length=50, validators=[solo_letras_espacios],null=True)
    noControl = models.CharField(max_length=9, unique=True, validators=[numero_control_validator],null=True)
    correo = models.EmailField(max_length=50, unique=True, validators=[EmailValidator(message='Ingrese un correo electrónico válido')],null=True)
    sexo = models.BooleanField(null=True)  # 1=Femenino, 0=Masculino
    fechaNacimiento = models.DateField(null=True)
    carrera = models.CharField(max_length=50, validators=[solo_letras_espacios])
    titulado = models.BooleanField(null=True)
    fechaEgreso = models.DateField(null=True)
    contraseña = models.CharField(max_length=128,null=True)
    tempPwd = models.CharField(max_length=128, blank=True, null=True)
    sesion = models.CharField(max_length=255, blank=True, null=True)

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
    contraseña = models.CharField(max_length=128)
    sesion = models.CharField(max_length=255, blank=True, null=True)
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
    fechaFin = models.DateField(null=True, blank=True)
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
# MODELO temporal de administrador
# ---------------------------
class AdministradorTemporal(models.Model):
    rfc = models.CharField(max_length=13, primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    carrera = models.CharField(max_length=100, blank=True, null=True)
    contraseña = models.CharField(max_length=128)  # ya encriptada
    fecha_creacion = models.DateTimeField(auto_now_add=True)

# ---------------------------
# MODELO temporal de egresado
# ---------------------------
class EgresadoTemporal(models.Model):
    curp = models.CharField(max_length=18, primary_key=True)
    nombre = models.CharField(max_length=100)
    no_control = models.CharField(max_length=20)
    correo = models.EmailField()
    sexo = models.BooleanField()
    fecha_nacimiento = models.DateField()
    carrera = models.CharField(max_length=100)
    titulado = models.BooleanField()
    fecha_egreso = models.DateField()
    contraseña = models.CharField(max_length=128)  # Hasheada
    fecha_creacion = models.DateTimeField(default=now)

# ---------------------------
# MODELOS de Secciones de Encuesta
# ---------------------------
class EncuestaS1(models.Model):
    # Opciones para el campo "sexo"
    SEXO_CHOICES = [
        (1, 'Femenino'),
        (0, 'Masculino')
    ]
    
    # Opciones para el campo "estadoCivil"
    ESTADO_CIVIL_CHOICES = [
        (1, 'Soltero'),
        (2, 'Casado')
    ]
    
    # Opciones para el campo "titulado"
    TITULADO_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "manejoPaquetes"
    MANEJO_PAQUETES_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    folioEncuestaS1 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    # Datos de la Imagen 1
    nombre = models.CharField(max_length=100, null=True)
    noControl = models.CharField(max_length=20, null=True)
    fechaNacimiento = models.DateField(null=True)
    curp = models.CharField(max_length=18, null=True)
    sexo = models.IntegerField(choices=SEXO_CHOICES, null=True)
    estadoCivil = models.IntegerField(choices=ESTADO_CIVIL_CHOICES, null=True)
    domicilio = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=50, null=True)
    cp = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=50, null=True)
    telefono = models.CharField(max_length=20, null=True)
    
    # Datos de la Imagen 2
    carrera = models.CharField(max_length=100, null=True)
    especialidad = models.CharField(max_length=100, null=True)
    fechaIngreso = models.DateField(null=True)
    fechaEgreso = models.DateField(null=True)
    titulado = models.IntegerField(choices=TITULADO_CHOICES, null=True)
    dominioIngles = models.IntegerField(help_text="Porcentaje de dominio", null=True)
    otroIdioma = models.CharField(max_length=50, blank=True, null=True)
    manejoPaquetes = models.IntegerField(choices=MANEJO_PAQUETES_CHOICES, null=True)
    especificarPaquetes = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return f"Perfil del Egresado - {self.nombre} - Encuesta {self.folioEncuesta}"

class EncuestaS2(models.Model):
    # Opciones para los campos de calificación
    CALIFICACION_CHOICES = [
        (4, 'Muy buena'),
        (3, 'Buena'),
        (2, 'Regular'),
        (1, 'Mala')
    ]
    
    folioEncuestaS2 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    # Campos basados en la imagen
    calidadDocentes = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        verbose_name="Calidad de docentes",
        null=True
    )
    
    planEstudios = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        verbose_name="Plan de estudios",
        null=True
    )
    
    oportunidadesProyectos = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        verbose_name="Oportunidades de participar en proyectos de investigación y desarrollo",
        null=True
    )
    
    enfasisInvestigacion = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        verbose_name="Énfasis que se le prestaba a la investigación dentro del proceso de enseñanza",
        null=True
    )
    
    satisfaccionCondiciones = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        verbose_name="Satisfacción con las condiciones de estudio",
        null=True
    )
    
    experienciaResidencia = models.IntegerField(
        choices=CALIFICACION_CHOICES,
        verbose_name="Experiencia obtenida a través de la residencia profesional",
        null=True
    )
    
    def __str__(self):
        return f"Pertinencia y disponibilidad de medios - Encuesta {self.folioEncuesta}"

class EncuestaS3(models.Model):
    # Opciones para el campo "actividad"
    ACTIVIDAD_CHOICES = [
        (1, 'Trabaja'),
        (2, 'Estudia'),
        (3, 'Estudia y trabaja'),
        (4, 'No estudia ni trabaja')
    ]
    
    # Opciones para el campo "tipoEstudio"
    TIPO_ESTUDIO_CHOICES = [
        (1, 'Especialidad'),
        (2, 'Maestría'),
        (3, 'Doctorado'),
        (4, 'Idiomas'),
        (5, 'Otra')
    ]
    
    # Opciones para el campo "tiempoObtenerEmpleo"
    TIEMPO_OBTENER_EMPLEO_CHOICES = [
        (1, 'Antes de Egresar'),
        (2, 'Menos de seis meses'),
        (3, 'Entre seis meses y un año'),
        (4, 'Más de un año')
    ]
    
    # Opciones para el campo "medioEmpleo"
    MEDIO_EMPLEO_CHOICES = [
        (1, 'Bolsa de trabajo del plantel'),
        (2, 'Contactos personales'),
        (3, 'Residencia Profesional'),
        (4, 'Medios masivos de comunicación'),
        (5, 'Otros')
    ]
    
    REQUISITOS_CONTRATACION_CHOICES = [
        (1, 'Competencias laborales'),
        (2, 'Titulo profesional'),
        (3, 'Examen de selección'),
        (4, 'Idioma extranjero'),
        (5, 'Actitudes y habilidades socio-comunicativas'),
        (6, 'Ninguno'),
        (7, 'Otro')
    ]
    
    # Opciones para el campo "idiomaUtiliza"
    IDIOMA_UTILIZA_CHOICES = [
        (1, 'Inglés'),
        (2, 'Francés'),
        (3, 'Alemán'),
        (4, 'Japones'),
        (5, 'Otros')
    ]
    
    # Opciones para el campo "antiguedad"
    ANTIGUEDAD_CHOICES = [
        (1, 'Menos de un año'),
        (2, 'Un año'),
        (3, 'Dos años'),
        (4, 'Tres años'),
        (5, 'Más de tres años')
    ]
    
    # Opciones para el campo "ingreso"
    INGRESO_CHOICES = [
        (1, 'Menos de cinco'),
        (2, 'Entre cinco y siete'),
        (3, 'Entre ocho y diez'),
        (4, 'Más de diez')
    ]
    
    # Opciones para el campo "nivelJerarquico"
    NIVEL_JERARQUICO_CHOICES = [
        (1, 'Técnico'),
        (2, 'Supervisor'),
        (3, 'Jefe de área'),
        (4, 'Funcionario'),
        (5, 'Directivo'),
        (6, 'Empresario')
    ]
    
    # Opciones para el campo "condicionTrabajo"
    CONDICION_TRABAJO_CHOICES = [
        (1, 'Base'),
        (2, 'Eventual'),
        (3, 'Contrato'),
        (4, 'Otros')
    ]
    
    # Opciones para el campo "relacionTrabajo"
    RELACION_TRABAJO_CHOICES = [
        (1, '0%'),
        (2, '20%'),
        (3, '40%'),
        (4, '60%'),
        (5, '80%'),
        (6, '100%')
    ]
    
    folioEncuestaS3 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    # Campos de Imagen 1
    actividad = models.IntegerField(choices=ACTIVIDAD_CHOICES, null=True)
    tipoEstudio = models.IntegerField(choices=TIPO_ESTUDIO_CHOICES, blank=True, null=True)
    tipoEstudioOtro = models.CharField(max_length=100, blank=True, null=True)
    especialidadInstitucion = models.CharField(max_length=200, blank=True, null=True)
    tiempoObtenerEmpleo = models.IntegerField(choices=TIEMPO_OBTENER_EMPLEO_CHOICES, blank=True, null=True)
    
    # Campos de Imagen 2
    medioEmpleo = models.IntegerField(choices=MEDIO_EMPLEO_CHOICES, blank=True, null=True)
    medioEmpleoOtro = models.CharField(max_length=100, blank=True, null=True)
    requisitosContratacion = models.IntegerField(choices=REQUISITOS_CONTRATACION_CHOICES, blank=True, null=True)
    requisitosContratacionOtro = models.CharField(max_length=100, blank=True, null=True)
    idiomaUtiliza = models.IntegerField(choices=IDIOMA_UTILIZA_CHOICES, blank=True, null=True)
    idiomaUtilizaOtro = models.CharField(max_length=50, blank=True, null=True)
    hablarPorcentaje = models.IntegerField(blank=True, null=True)
    escribirPorcentaje = models.IntegerField(blank=True, null=True)
    leerPorcentaje = models.IntegerField(blank=True, null=True)
    escucharPorcentaje = models.IntegerField(blank=True, null=True)
    
    # Campos de Imagen 3
    antiguedad = models.IntegerField(choices=ANTIGUEDAD_CHOICES, blank=True, null=True)
    anioIngreso = models.IntegerField(blank=True, null=True)
    ingreso = models.IntegerField(choices=INGRESO_CHOICES, blank=True, null=True)
    nivelJerarquico = models.IntegerField(choices=NIVEL_JERARQUICO_CHOICES, blank=True, null=True)
    condicionTrabajo = models.IntegerField(choices=CONDICION_TRABAJO_CHOICES, blank=True, null=True)
    condicionTrabajoOtro = models.CharField(max_length=100, blank=True, null=True)
    relacionTrabajo = models.IntegerField(choices=RELACION_TRABAJO_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return f"Ubicación Laboral - Encuesta {self.folioEncuesta}"

class EncuestaS3Empresa(models.Model):
    # Opciones para el campo "tipoOrganismo"
    TIPO_ORGANISMO_CHOICES = [
        (1, 'Público'),
        (2, 'Privado'),
        (3, 'Social')
    ]
    
    # Opciones para el campo "sectorPrimario"
    SECTOR_PRIMARIO_CHOICES = [
        (1, 'Agroindustrial'),
        (2, 'Pesquero'),
        (3, 'Minero'),
        (4, 'Otros')
    ]
    
    # Opciones para el campo "sectorSecundario"
    SECTOR_SECUNDARIO_CHOICES = [
        (1, 'Industrial'),
        (2, 'Construcción'),
        (3, 'Petrolero'),
        (4, 'Otros')
    ]
    
    # Opciones para el campo "sectorTerciario"
    SECTOR_TERCIARIO_CHOICES = [
        (1, 'Educativo'),
        (2, 'Turismo'),
        (3, 'Comercio'),
        (4, 'Servicios financieros'),
        (5, 'Otros')
    ]
    
    # Opciones para el campo "tamanoEmpresa"
    TAMANO_EMPRESA_CHOICES = [
        (1, 'Microempresa (1-30)'),
        (2, 'Pequeña (31-100)'),
        (3, 'Mediana (101-500)'),
        (4, 'Grande (más de 500)')
    ]
    
    folioEncuestaS3Empresa = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    # Datos de la Imagen 1 (III.12)
    tipoOrganismo = models.IntegerField(choices=TIPO_ORGANISMO_CHOICES, null=True)
    giroActividad = models.CharField(max_length=100, null=True)
    razonSocial = models.CharField(max_length=150, null=True)
    domicilio = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=50, null=True)
    cp = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)
    telefono = models.CharField(max_length=20, null=True)
    nombreJefeInmediato = models.CharField(max_length=100, null=True)
    puestoJefeInmediato = models.CharField(max_length=50, null=True)
    
    # Datos de la Imagen 2 (III.13 y III.14)
    sectorPrimario = models.IntegerField(choices=SECTOR_PRIMARIO_CHOICES, blank=True, null=True)
    sectorPrimarioOtro = models.CharField(max_length=50, blank=True, null=True)
    sectorSecundario = models.IntegerField(choices=SECTOR_SECUNDARIO_CHOICES, blank=True, null=True)
    sectorSecundarioOtro = models.CharField(max_length=50, blank=True, null=True)
    sectorTerciario = models.IntegerField(choices=SECTOR_TERCIARIO_CHOICES, blank=True, null=True)
    sectorTerciarioOtro = models.CharField(max_length=50, blank=True, null=True)
    tamanoEmpresa = models.IntegerField(choices=TAMANO_EMPRESA_CHOICES, null=True)
    
    def __str__(self):
        return f"Datos de Empresa - {self.razonSocial} - Encuesta {self.folioEncuesta}"

class EncuestaS4(models.Model):
    # Constante para los valores de calificación
    EFICIENCIA_CHOICES = [
        (1, 'Muy eficiente'),
        (2, 'Eficiente'),
        (3, 'Poco eficiente'),
        (4, 'Deficiente')
    ]
    
    FORMACION_CHOICES = [
        (1, 'Excelente'),
        (2, 'Bueno'),
        (3, 'Regular'),
        (4, 'Malo'),
        (5, 'Pésimo')
    ]
    
    UTILIDAD_CHOICES = [
        (1, 'Excelente'),
        (2, 'Bueno'),
        (3, 'Regular'),
        (4, 'Malo'),
        (5, 'Pésimo')
    ]
    
    VALORACION_CHOICES = [
        (1, '1(poco)'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5(mucho)')
    ]
    
    folioEncuestaS4 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    eficiencia = models.IntegerField(choices=EFICIENCIA_CHOICES, blank=True, null=True)
    formacion = models.IntegerField(choices=FORMACION_CHOICES, blank=True, null=True)
    utilidad = models.IntegerField(choices=UTILIDAD_CHOICES, blank=True, null=True)
    # Aspectos valorados para contratación (IV.4)
    areaCampoEstudio = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Área o campo de estudio",
        null=True
    )
    
    titulacion = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Titulación",
        null=True
    )
    
    experienciaLaboral = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Experiencia laboral/práctica",
        null=True
    )
    
    competenciaLaboral = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Competencia laboral",
        null=True
    )
    
    posicionamientoInstitucion = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Posicionamiento de la institución",
        null=True
    )
    
    conocimientoIdiomas = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Conocimiento de idiomas",
        null=True
    )
    
    recomendacionesReferencias = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Recomendaciones/referencias",
        null=True
    )
    
    personalidadActitudes = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Personalidad/actitudes",
        null=True
    )
    
    capacidadLiderazgo = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Capacidad de liderazgo",
        null=True
    )
    
    otrosAspectos = models.IntegerField(
        choices=VALORACION_CHOICES,
        verbose_name="Otros",
        null=True
    )
    
    def __str__(self):
        return f"Desempeño Profesional - Encuesta {self.folioEncuesta}"

class EncuestaS5(models.Model):
    # Opciones para los campos Sí/No
    SI_NO_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    folioEncuestaS5 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    # Sección V - Actualización de conocimientos
    cursosActualizacion = models.IntegerField(
        choices=SI_NO_CHOICES,
        verbose_name="Le gustaría tomar cursos de actualización",
        null=True
    )
    cursosActualizacionCuales = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="¿Qué cursos de actualización le gustaría tomar?"
    )
    
    tomarPosgrado = models.IntegerField(
        choices=SI_NO_CHOICES,
        verbose_name="Le gustaría tomar algún Posgrado",
        null=True
    )
    tomarPosgradoCual = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="¿Qué posgrado le gustaría tomar?"
    )
    
    # Sección VI - Participación social
    perteneceOrganizacionesSociales = models.IntegerField(
        choices=SI_NO_CHOICES,
        verbose_name="Pertenece a organizaciones sociales",
        null=True
    )
    organizacionesSocialesCuales = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="¿A cuáles organizaciones sociales pertenece?"
    )
    
    perteneceOrganismosProfesionistas = models.IntegerField(
        choices=SI_NO_CHOICES,
        verbose_name="Pertenece a organismos de profesionistas",
        null=True
    )
    organismosProfesionistasCuales = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="¿A cuáles organismos de profesionistas pertenece?"
    )
    
    perteneceAsociacionEgresados = models.IntegerField(
        choices=SI_NO_CHOICES,
        verbose_name="Pertenece a la asociación de egresados",
        null=True
    )
    
    # Sección VIII - Comentarios y sugerencias
    comentariosSugerencias = models.TextField(
        blank=True,
        null=True,
        verbose_name="Opinión o recomendación para mejorar la formación profesional de un egresado de su carrera"
    )
    
    def __str__(self):
        return f"Expectativas y Participación Social - Encuesta {self.folioEncuesta}"

# ---------------------------
# MODELOS de Anexos
# ---------------------------
class AnexoS1(models.Model):
    TITULO_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    RAZON_NO_TITULO_CHOICES = [
        (1, 'Compromiso laboral'),
        (2, 'Falta de tiempo'),
        (3, 'Falta de apoyo institucional'),
        (4, 'Otras')
    ]
    
    folioAnexoS1 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    # Anexo1
    nombreCompleto = models.CharField(max_length=100, blank=True, null=True)
    redesSociales = models.CharField(max_length=100, blank=True, null=True)
    fechaIngreso = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    fechaEgreso = models.DateField(blank=True, null=True)

    # Anexo2
    titulado = models.IntegerField(choices=TITULO_CHOICES, null=True)
    razonNoTitulo = models.IntegerField(
        choices=RAZON_NO_TITULO_CHOICES,
        blank=True,
        null=True
    )
    razonNoTituloOtra = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['folioEncuesta'], name='unique_folio_anexos1')
        ]

    def __str__(self):
        return f"Anexo S1 - Encuesta {self.folioEncuesta}"

class AnexoS2(models.Model):
    # Opciones para el campo "trabaja" (Anexo3)
    TRABAJA_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "razonNoTrabaja" (Anexo3)
    RAZON_NO_TRABAJA_CHOICES = [
        (1, 'Estudio un Posgrado'),
        (2, 'Por razones de salud'),
        (3, 'Ajustes propios de la empresa'),
        (4, 'No he encontrado un trabajo relacionado a lo que estudié'),
        (5, 'Otras')
    ]
    
    # Opciones para el campo "relacionTrabajoCarrera" (Anexo4)
    RELACION_TRABAJO_CARRERA_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "antiguedad" (Anexo4)
    ANTIGUEDAD_CHOICES = [
        (1, '0-3 Meses'),
        (2, '4-6 Meses'),
        (3, '6 Meses - 1 Año'),
        (4, '1-5 Años'),
        (5, '6 años o más')
    ]
    
    # Opciones para el campo "tiempoTrabajoRelacionado" (Anexo4)
    TIEMPO_TRABAJO_RELACIONADO_CHOICES = [
        (1, 'Al egresar ya contaba con un trabajo'),
        (2, 'Menos de 6 meses'),
        (3, 'Más de 1 año'),
        (4, 'Aún no lo consigo')
    ]
    
    # Opciones para el campo "sector" (Anexo5)
    SECTOR_CHOICES = [
        (1, 'Sector privado'),
        (2, 'Sector público'),
        (3, 'En empresa propia'),
        (4, 'Otro')
    ]
    
    # Opciones para el campo "rol" (Anexo5)
    ROL_CHOICES = [
        (1, 'Dirección/gerencia'),
        (2, 'Jefatura'),
        (3, 'Supervisión'),
        (4, 'Coordinador'),
        (5, 'Empleado'),
        (6, 'Dueño de empresa'),
        (7, 'Otras')
    ]
    
    # Opciones para el campo "area" (Anexo5)
    AREA_CHOICES = [
        (1, 'Producción'),
        (2, 'Ambiental'),
        (3, 'Seguridad'),
        (4, 'Recursos Financiero'),
        (5, 'Mantenimiento'),
        (6, 'Recursos Humanos'),
        (7, 'Otras')
    ]
    
    # Opciones para el campo "medioTrabajo" (Anexo6)
    MEDIO_TRABAJO_CHOICES = [
        (1, 'Bolsa de trabajo del TecNM/ITVer'),
        (2, 'Anuncio en internet'),
        (3, 'Recomendación de colegas'),
        (4, 'Residencias profesionales'),
        (5, 'Otras')
    ]
    
    # Opciones para el campo "satisfaccion" (Anexo6)
    SATISFACCION_CHOICES = [
        (1, 'Muy satisfecho'),
        (2, 'Satisfecho'),
        (3, 'Poco satisfecho'),
        (4, 'Insatisfecho')
    ]
    
    folioAnexoS2 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)

    # Anexo3
    trabaja = models.IntegerField(choices=TRABAJA_CHOICES, null=True)
    razonNoTrabaja = models.IntegerField(choices=RAZON_NO_TRABAJA_CHOICES, blank=True, null=True)
    razonNoTrabajaOtra = models.CharField(max_length=100, blank=True, null=True)

    # Anexo4
    relacionTrabajoCarrera = models.IntegerField(choices=RELACION_TRABAJO_CARRERA_CHOICES, blank=True, null=True)
    antiguedad = models.IntegerField(choices=ANTIGUEDAD_CHOICES, blank=True, null=True)
    tiempoTrabajoRelacionado = models.IntegerField(choices=TIEMPO_TRABAJO_RELACIONADO_CHOICES, blank=True, null=True)
    razonNoConseguirTrabajo = models.CharField(max_length=100, blank=True, null=True)

    # Anexo5
    sector = models.IntegerField(choices=SECTOR_CHOICES, blank=True, null=True)
    sectorOtro = models.CharField(max_length=100, blank=True, null=True)
    rol = models.IntegerField(choices=ROL_CHOICES, blank=True, null=True)
    rolOtro = models.CharField(max_length=100, blank=True, null=True)
    area = models.IntegerField(choices=AREA_CHOICES, blank=True, null=True)
    areaOtra = models.CharField(max_length=100, blank=True, null=True)

    # Anexo6
    medioTrabajo = models.IntegerField(choices=MEDIO_TRABAJO_CHOICES, blank=True, null=True)
    medioTrabajoOtro = models.CharField(max_length=100, blank=True, null=True)
    satisfaccion = models.IntegerField(choices=SATISFACCION_CHOICES, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['folioEncuesta'], name='unique_folio_anexos2')
        ]


    def __str__(self):
        return f"Anexo S2 - Encuesta {self.folioEncuesta}"

class AnexoS3(models.Model):
    # Opciones para el campo "competencias" (Anexo7)
    COMPETENCIAS_CHOICES = [
        (1, 'Totalmente'),
        (2, 'Suficiente'),
        (3, 'Poco'),
        (4, 'Nada')
    ]
    
    # Opciones para el campo "satisfaccion" (Anexo7)
    SATISFACCION_CHOICES = [
        (1, 'Muy Satisfecho'),
        (2, 'Satisfecho'),
        (3, 'Poco Satisfecho'),
        (4, 'Insatisfecho')
    ]
    
    # Opciones para el campo "educativo" (Anexo7)
    EDUCATIVO_CHOICES = [
        (1, 'Manejo de softwares'),
        (2, 'Manejo de normas nacionales e internacionales'),
        (3, 'Evaluación de proyectos de inversión'),
        (4, 'Habilidades directivas'),
        (5, 'Otras')
    ]
    
    # Opciones para el campo "contacto" (Anexo8)
    CONTACTO_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "participar" (Anexo8)
    PARTICIPAR_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "aporte" (Anexo8)
    APORTE_CHOICES = [
        (1, 'Impartiendo un curso o conferencia'),
        (2, 'Apoyar para una visita industrial donde laboras'),
        (3, 'Apoyar para la realización de Residencias Profesionales'),
        (4, 'Apoyar para realizar investigaciones'),
        (5, 'Apoyar a jóvenes para la Educación Dual'),
        (6, 'Donativos'),
        (7, 'Otras')
    ]
    
    folioAnexoS3 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    # Anexo7
    competencias = models.IntegerField(choices=COMPETENCIAS_CHOICES, null=True)
    satisfaccion = models.IntegerField(choices=SATISFACCION_CHOICES, null=True)
    educativo = models.IntegerField(choices=EDUCATIVO_CHOICES, null=True)
    educativoOtro = models.CharField(max_length=100, blank=True, null=True)
    
    # Anexo8
    contacto = models.IntegerField(choices=CONTACTO_CHOICES, null=True)
    participar = models.IntegerField(choices=PARTICIPAR_CHOICES, null=True)
    aporte = models.IntegerField(choices=APORTE_CHOICES, blank=True, null=True)
    aporteOtro = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['folioEncuesta'], name='unique_folio_anexos3')
        ]

    
    def __str__(self):
        return f"Anexo S3 - Encuesta {self.folioEncuesta}"

class AnexoS4(models.Model):
    # Opciones para el campo "herramientas" (Anexo9)
    HERRAMIENTAS_CHOICES = [
        (1, 'Documentos técnicos'),
        (2, 'Planos de ingeniería'),
        (3, 'Softwares'),
        (4, 'Normas nacionales o internacionales'),
        (5, 'Otras')
    ]
    
    # Opciones para el campo "colabora" (Anexo9)
    COLABORA_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "tipoInvestigacion" (Anexo9)
    TIPO_INVESTIGACION_CHOICES = [
        (1, 'Aplicada'),
        (2, 'Experimental'),
        (3, 'Documental'),
        (4, 'Descriptiva'),
        (5, 'Otras')
    ]
    
    # Opciones para el campo "participaRedes" (Anexo10)
    PARTICIPA_REDES_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "certificacion" (Anexo10)
    CERTIFICACION_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "servicios" (Anexo10)
    SERVICIOS_CHOICES = [
        (1, 'Asesoría o consultoría'),
        (2, 'Peritaje'),
        (3, 'Certificación'),
        (4, 'Ninguno'),
        (5, 'Otras')
    ]
    
    # Opciones para el campo "idiomas" (Anexo10)
    IDIOMAS_CHOICES = [
        (1, 'Inglés'),
        (2, 'Frances'),
        (3, 'Alemán'),
        (4, 'Italiano'),
        (5, 'Otras')
    ]
    
    # Opciones para el campo "publicacion" (Anexo11)
    PUBLICACION_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "documentos" (Anexo11)
    DOCUMENTOS_CHOICES = [
        (0, 'Manuales operativos'),
        (1, 'Procedimientos'),
        (2, 'Lineamientos'),
        (3, 'Informes técnicos'),
        (4, 'Otro')
    ]
    
    # Opciones para el campo "calidad" (Anexo11)
    CALIDAD_CHOICES = [
        (0, 'Calidad'),
        (1, 'Ambiental'),
        (2, 'Seguridad'),
        (3, 'Otras')
    ]
    
    # Opciones para el campo "asociacion" (Anexo12)
    ASOCIACION_CHOICES = [
        (1, 'Sí'),
        (0, 'No')
    ]
    
    # Opciones para el campo "etica" (Anexo12)
    ETICA_CHOICES = [
        (1, 'Aplicar las normas básicas de una empresa'),
        (2, 'Aplicar reglas de cortesía que demuestran respeto por los demás'),
        (3, 'Asumir un comportamiento adecuado para la buena convivencia'),
        (4, 'Establecer una serie de normas como guía de conducta'),
        (5, 'Ninguna de las anteriores')
    ]
    
    folioAnexoS4 = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    
    # Anexo9
    herramientas = models.IntegerField(choices=HERRAMIENTAS_CHOICES, null=True)
    herramientasOtra = models.CharField(max_length=100, blank=True, null=True)
    colabora = models.IntegerField(choices=COLABORA_CHOICES, null=True)
    tipoInvestigacion = models.IntegerField(choices=TIPO_INVESTIGACION_CHOICES, blank=True, null=True)
    tipoInvestigacionOtra = models.CharField(max_length=100, blank=True, null=True)
    
    # Anexo10
    participaRedes = models.IntegerField(choices=PARTICIPA_REDES_CHOICES, null=True)
    certificacion = models.IntegerField(choices=CERTIFICACION_CHOICES, null=True)
    certificacionCuales = models.CharField(max_length=200, blank=True, null=True)
    servicios = models.IntegerField(choices=SERVICIOS_CHOICES, null=True)
    serviciosOtro = models.CharField(max_length=100, blank=True, null=True)
    idiomas = models.IntegerField(choices=IDIOMAS_CHOICES, null=True)
    idiomasOtro = models.CharField(max_length=100, blank=True, null=True)
    
    # Anexo11
    publicacion = models.IntegerField(choices=PUBLICACION_CHOICES, null=True)
    publicacionEspecifique = models.CharField(max_length=200, blank=True, null=True)
    documentos = models.IntegerField(choices=DOCUMENTOS_CHOICES, null=True)
    documentosOtro = models.CharField(max_length=100, blank=True, null=True)
    calidad = models.IntegerField(choices=CALIDAD_CHOICES, null=True)
    calidadOtra = models.CharField(max_length=100, blank=True, null=True)
    
    # Anexo12
    asociacion = models.IntegerField(choices=ASOCIACION_CHOICES, null=True)
    asociacionEspecifique = models.CharField(max_length=200, blank=True, null=True)
    etica = models.IntegerField(choices=ETICA_CHOICES, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['folioEncuesta'], name='unique_folio_anexos4')
        ]
    
    def __str__(self):
        return f"Anexo S4 - Encuesta {self.folioEncuesta}"

# ---------------------------
# MODELOS de Selección Múltiple
# ---------------------------
class OpcionesSeleccionMultiple(models.Model):
    CODIGO_PREGUNTA_CHOICES = [
        ('III.4', 'Requisitos de contratación'),
        ('III.5', 'Idioma que utiliza en su trabajo')
    ]
    
    idOpcion = models.BigAutoField(primary_key=True)
    codigoPregunta = models.CharField(max_length=5, choices=CODIGO_PREGUNTA_CHOICES,null=True)
    textoOpcion = models.CharField(max_length=100,null=True)
    valorNumerico = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['codigoPregunta', 'valorNumerico']
    
    def __str__(self):
        return f"{self.codigoPregunta} - {self.textoOpcion}"
class RespuestaSeleccionMultiple(models.Model):
    id = models.BigAutoField(primary_key=True)
    folioEncuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE,null=True)
    opcion = models.ForeignKey(OpcionesSeleccionMultiple, on_delete=models.CASCADE,null=True)
    
    class Meta:
        unique_together = (('folioEncuesta', 'opcion'),)
        
    def __str__(self):
        return f"{self.opcion.codigoPregunta} - {self.opcion.textoOpcion} - Encuesta {self.folioEncuesta}"

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
