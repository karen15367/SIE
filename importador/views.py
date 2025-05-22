#importador/views.py

import pandas as pd
from datetime import date
from django.db.models import Count
from django.shortcuts import render
from django.shortcuts import render, redirect
from core.models import Egresado, Encuesta, EncuestaS1, EncuestaS2, EncuestaS3, EncuestaS4, EncuestaS5,EncuestaS3Empresa
from core.models import AnexoS1, AnexoS2, AnexoS3, AnexoS4
from django.http import HttpResponse
import traceback
from datetime import datetime



# Helper para Sí/No → 1/0
def conv_si_no(valor):
    if pd.isna(valor):
        return None
    texto = str(valor).strip().lower()
    if texto in ['sí', 'si', '1', 'true', 'verdadero']:
        return 1
    elif texto in ['no', '0', 'false', 'falso']:
        return 0
    return None

def map_razon_no_titulo(valor):
    if pd.isna(valor): return None
    texto = str(valor).strip().lower()
    if 'compromiso' in texto:
        return 1
    elif 'tiempo' in texto:
        return 2
    elif 'apoyo' in texto:
        return 3
    elif 'otra' in texto:
        return 4
    return None

# Mapeos para encuesta
#EncuestaS1
def map_sexo(valor):
    if not valor: return None
    mapa = {
        "Femenino": 1,
        "Masculino": 0
    }
    return mapa.get(str(valor).strip())

def map_estado_civil(valor):
    if not valor: return None
    mapa = {
        "Soltero": 1,
        "Casado": 2
    }
    return mapa.get(str(valor).strip())

def map_titulado(valor):
    if not valor: return None
    mapa = {
        "Sí": 1,
        "No": 0
    }
    return mapa.get(str(valor).strip())

def map_manejo_paquetes(valor):
    if not valor: return None
    mapa = {
        "Sí": 1,
        "No": 0
    }
    return mapa.get(str(valor).strip())

#EncuestaS2
def map_calificacion(valor):
    if not valor: return None
    mapa = {
        "Muy Buena": 4,
        "Buena": 3,
        "Regular": 2,
        "Mala": 1
    }
    return mapa.get(str(valor).strip())

#EncuestaS3
def map_actividad(valor):
    if not valor: return None
    mapa = {
        "Trabaja": 1,
        "Estudia": 2,
        "Estudia y trabaja": 3,
        "No estudia ni trabaja": 4
    }
    return mapa.get(str(valor).strip())

def map_tipo_estudio(valor):
    if not valor: return None
    mapa = {
        "Especialidad": 1,
        "Maestría": 2,
        "Doctorado": 3,
        "Idiomas": 4,
        "Otra": 5
    }
    return mapa.get(str(valor).strip())

def map_tiempo_obtener_empleo(valor):
    if not valor: return None
    mapa = {
        "Antes de Egresar": 1,
        "Menos de seis meses": 2,
        "Entre seis meses y un año": 3,
        "Más de un año": 4
    }
    return mapa.get(str(valor).strip())

def map_medio_empleo(valor):
    if not valor: return None
    mapa = {
        "Bolsa de trabajo del plantel": 1,
        "Contactos personales": 2,
        "Residencia Profesional": 3,
        "Medios masivos de comunicación": 4,
        "Otros": 5
    }
    return mapa.get(str(valor).strip())

def map_requisitos_contratacion(valor):
    if not valor: return None
    mapa = {
        "Competencias laborales": 1,
        "Titulo profesional": 2,
        "Examen de selección": 3,
        "Idioma extranjero": 4,
        "Actitudes y habilidades socio-comunicativas": 5,
        "Ninguno": 6,
        "Otro": 7
    }
    return mapa.get(str(valor).strip())

def map_idioma_utiliza(valor):
    if not valor: return None
    mapa = {
        "Inglés": 1,
        "Francés": 2,
        "Alemán": 3,
        "Japones": 4,
        "Otros": 5
    }
    return mapa.get(str(valor).strip())

def map_antiguedad(valor):
    if not valor: return None
    mapa = {
        "Menos de un año": 1,
        "Un año": 2,
        "Dos años": 3,
        "Tres años": 4,
        "Más de tres años": 5
    }
    return mapa.get(str(valor).strip())

def map_ingreso(valor):
    if not valor: return None
    mapa = {
        "Menos de cinco": 1,
        "Entre cinco y siete": 2,
        "Entre ocho y diez": 3,
        "Más de diez": 4
    }
    return mapa.get(str(valor).strip())

def map_nivel_jerarquico(valor):
    if not valor: return None
    mapa = {
        "Técnico": 1,
        "Supervisor": 2,
        "Jefe de área": 3,
        "Funcionario": 4,
        "Directivo": 5,
        "Empresario": 6
    }
    return mapa.get(str(valor).strip())

def map_condicion_trabajo(valor):
    if not valor: return None
    mapa = {
        "Base": 1,
        "Eventual": 2,
        "Contrato": 3,
        "Otros": 4
    }
    return mapa.get(str(valor).strip())

def map_relacion_trabajo(valor):
    if not valor: return None
    mapa = {
        "0%": 1,
        "20%": 2,
        "40%": 3,
        "60%": 4,
        "80%": 5,
        "100%": 6
    }
    return mapa.get(str(valor).strip())

#EncuestaS3Empresa
def map_tipo_organismo(valor):
    if not valor: return None
    mapa = {
        "Público": 1,
        "Privado": 2,
        "Social": 3
    }
    return mapa.get(str(valor).strip())

def map_sector_primario(valor):
    if not valor: return None
    mapa = {
        "Agroindustrial": 1,
        "Pesquero": 2,
        "Minero": 3,
        "Otros": 4
    }
    return mapa.get(str(valor).strip())

def map_sector_secundario(valor):
    if not valor: return None
    mapa = {
        "Industrial": 1,
        "Construcción": 2,
        "Petrolero": 3,
        "Otros": 4
    }
    return mapa.get(str(valor).strip())

def map_sector_terciario(valor):
    if not valor: return None
    mapa = {
        "Educativo": 1,
        "Turismo": 2,
        "Comercio": 3,
        "Servicios financieros": 4,
        "Otros": 5
    }
    return mapa.get(str(valor).strip())

def map_tamano_empresa(valor):
    if not valor: return None
    mapa = {
        "Microempresa (1-30)": 1,
        "Pequeña (31-100)": 2,
        "Mediana (101-500)": 3,
        "Grande (más de 500)": 4
    }
    return mapa.get(str(valor).strip())

#EncuestaS4
def map_eficiencia(valor):
    if not valor: return None
    mapa = {
        "Muy eficiente": 1,
        "Eficiente": 2,
        "Poco eficiente": 3,
        "Deficiente": 4
    }
    return mapa.get(str(valor).strip())

def map_formacion(valor):
    if not valor: return None
    mapa = {
        "Excelente": 1,
        "Bueno": 2,
        "Regular": 3,
        "Malo": 4,
        "Pésimo": 5
    }
    return mapa.get(str(valor).strip())

def map_utilidad(valor):
    if not valor: return None
    mapa = {
        "Excelente": 1,
        "Bueno": 2,
        "Regular": 3,
        "Malo": 4,
        "Pésimo": 5
    }
    return mapa.get(str(valor).strip())

def map_valoracion(valor):
    if not valor: return None
    mapa = {
        "1(poco)": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5(mucho)": 5
    }
    return mapa.get(str(valor).strip())

#mapeo para Anexo 
#AnexoS1
def map_razon_no_titulo(valor):
    if not valor: return None
    mapa = {
        "Compromiso laboral": 1,
        "Falta de tiempo": 2,
        "Falta de apoyo institucional": 3,
        "Otras": 4
    }
    return mapa.get(str(valor).strip())

#AnexoS2
def map_razon_no_trabaja(valor):
    if not valor: return None
    mapa = {
        "Estudio un Posgrado": 1,
        "Por razones de salud": 2,
        "Ajustes propios de la empresa": 3,
        "No he encontrado un trabajo relacionado a lo que estudié": 4,
        "Otras": 5
    }
    return mapa.get(str(valor).strip())

def map_relacion_trabajo_carrera(valor):
    return conv_si_no(valor)

def map_antiguedad(valor):
    if not valor: return None
    mapa = {
        "0-3 Meses": 1,
        "4-6 Meses": 2,
        "6 Meses - 1 Año": 3,
        "1-5 Años": 4,
        "6 años o más": 5
    }
    return mapa.get(str(valor).strip())

def map_tiempo_trabajo_relacionado(valor):
    if not valor: return None
    mapa = {
        "Al egresar ya contaba con un trabajo": 1,
        "Menos de 6 meses": 2,
        "Más de 1 año": 3,
        "Aún no lo consigo": 4
    }
    return mapa.get(str(valor).strip())

def map_sector(valor):
    if not valor: return None
    mapa = {
        "Sector privado": 1,
        "Sector público": 2,
        "En empresa propia": 3,
        "Otro": 4
    }
    return mapa.get(str(valor).strip())

def map_rol(valor):
    if not valor: return None
    mapa = {
        "Dirección/gerencia": 1,
        "Jefatura": 2,
        "Supervisión": 3,
        "Coordinador": 4,
        "Empleado": 5,
        "Dueño de empresa": 6,
        "Otras": 7
    }
    return mapa.get(str(valor).strip())

def map_area(valor):
    if not valor: return None
    mapa = {
        "Producción": 1,
        "Ambiental": 2,
        "Seguridad": 3,
        "Recursos Financiero": 4,
        "Mantenimiento": 5,
        "Recursos Humanos": 6,
        "Otras": 7
    }
    return mapa.get(str(valor).strip())

def map_medio_trabajo(valor):
    if not valor: return None
    mapa = {
        "Bolsa de trabajo del TecNM/ITVer": 1,
        "Anuncio en internet": 2,
        "Recomendación de colegas": 3,
        "Residencias profesional": 4,
        "Otras": 5
    }
    return mapa.get(str(valor).strip())

def map_satisfaccion(valor):
    if not valor: return None
    mapa = {
        "Muy satisfecho": 1,
        "Satisfecho": 2,
        "Poco satisfecho": 3,
        "Insatisfecho": 4
    }
    return mapa.get(str(valor).strip())

#AnexoS3
def map_competencias(valor):
    if not valor: return None
    mapa = {
        "Totalmente": 1,
        "Suficiente": 2,
        "Poco": 3,
        "Nada": 4
    }
    return mapa.get(str(valor).strip())

def map_satisfaccion_formacion(valor):
    if not valor: return None
    mapa = {
        "Muy Satisfecho": 1,
        "Satisfecho": 2,
        "Poco Satisfecho": 3,
        "Insatisfecho": 4
    }
    return mapa.get(str(valor).strip())

def map_educativo(valor):
    if not valor: return None
    mapa = {
        "Manejo de softwares": 1,
        "Manejo de normas nacionales e internacionales": 2,
        "Evaluación de proyectos de inversión": 3,
        "Habilidades directivas": 4,
        "Otras": 5
    }
    return mapa.get(str(valor).strip())

def map_contacto(valor):
    return conv_si_no(valor)

def map_participar(valor):
    return conv_si_no(valor)

def map_aporte(valor):
    if not valor: return None
    mapa = {
        "Impartiendo un curso o conferencia": 1,
        "Apoyar para una visita industrial donde laboras": 2,
        "Apoyar para la realización de Residencias Profesionales": 3,
        "Apoyar para realizar investigaciones": 4,
        "Apoyar a jóvenes para la Educación Dual": 5,
        "Donativos": 6,
        "Otras": 7
    }
    return mapa.get(str(valor).strip())

#AnexoS4
def map_herramientas(valor):
    if not valor: return None
    mapa = {
        "Documentos técnicos": 1,
        "Planos de ingeniería": 2,
        "Softwares": 3,
        "Normas nacionales o internacionales": 4,
        "Otras": 5
    }
    return mapa.get(str(valor).strip())

def map_colabora(valor):
    return conv_si_no(valor)

def map_tipo_investigacion(valor):
    if not valor: return None
    mapa = {
        "Aplicada": 1,
        "Experimental": 2,
        "Documental": 3,
        "Descriptiva": 4,
        "Otras": 5
    }
    return mapa.get(str(valor).strip())

def map_participa_redes(valor):
    return conv_si_no(valor)

def map_certificacion(valor):
    return conv_si_no(valor)

def map_servicios(valor):
    if not valor: return None
    mapa = {
        "Asesoría o consultoría": 1,
        "Peritaje": 2,
        "Certificación": 3,
        "Ninguno": 4,
        "Otras": 5
    }
    return mapa.get(str(valor).strip())

def map_idiomas(valor):
    if not valor: return None
    mapa = {
        "Inglés": 1,
        "Frances": 2,
        "Alemán": 3,
        "Italiano": 4,
        "Otro": 5
    }
    return mapa.get(str(valor).strip())

def map_publicacion(valor):
    return conv_si_no(valor)

def map_documentos(valor):
    if not valor: return None
    mapa = {
        "Manuales operativos": 0,
        "Procedimientos": 1,
        "Lineamientos": 2,
        "Informes técnicos": 3,
        "Otro": 4
    }
    return mapa.get(str(valor).strip())

def map_calidad(valor):
    if not valor: return None
    mapa = {
        "Calidad": 0,
        "Ambiental": 1,
        "Seguridad": 2,
        "Otras": 3
    }
    return mapa.get(str(valor).strip())

def map_asociacion(valor):
    return conv_si_no(valor)

def map_etica_anexo(valor):
    if not valor: return None
    mapa = {
        "Aplicar las Normas básicas de una empresa": 1,
        "Aplicar reglas de cortesía que demuestran respeto por los demás": 2,
        "Asumir un comportamiento adecuado para la buena convivencia": 3,
        "Establecer una serie de normas como guía de conducta": 4,
        "Ninguna de las anteriores": 5
    }
    return mapa.get(str(valor).strip())

#convertidor de fecha
def convertir_fecha(fecha_str):
    try:
        if pd.isna(fecha_str):
            return None
        return datetime.strptime(str(fecha_str).strip(), "%d-%m-%Y").date()
    except ValueError:
        return None

# Resumen de importación
def resumen_importaciones(request):
    # Agrupación por tipo y lapso
    encuesta_stats = Encuesta.objects.values('lapso').annotate(total=Count('folioEncuesta')).order_by('lapso')
    anexo_stats = AnexoS1.objects.select_related('folioEncuesta').values('folioEncuesta__lapso').annotate(total=Count('folioAnexoS1')).order_by('folioEncuesta__lapso')

    # Reorganizar para una sola tabla
    resumen = []

    for e in encuesta_stats:
        resumen.append({
            'tipo': 'Encuesta',
            'lapso': e['lapso'],
            'total': e['total']
        })

    for a in anexo_stats:
        resumen.append({
            'tipo': 'Anexo',
            'lapso': a['folioEncuesta__lapso'],
            'total': a['total']
        })

    return render(request, 'resumen_importaciones.html', {'resumen': resumen})


def procesar_excel_encuesta(request):
    if request.method != 'POST' or not request.FILES.get('archivo_excel'):
        return render(request, 'importar_encuesta.html', {
            'errores': ["Debes seleccionar un archivo Excel para importar."]
        })
    else:
        archivo = request.FILES['archivo_excel']
        hojas = pd.read_excel(archivo, sheet_name=None)
        print("Archivo recibido")
        # Función auxiliar para buscar la hoja aunque el nombre esté cortado
        def buscar_hoja(nombre_busqueda, hojas_dict):
            for clave in hojas_dict.keys():
                if nombre_busqueda.lower() in clave.lower():
                    return hojas_dict[clave]
            return None

        # Buscar las hojas con nombres incompletos
        hoja_s1 = buscar_hoja("perfil del egresado", hojas)
        hoja_s2 = buscar_hoja("pertinencia", hojas)
        hoja_s3 = buscar_hoja("ubicación laboral", hojas)
        hoja_s3e = buscar_hoja("empresa", hojas)
        hoja_s4 = buscar_hoja("desempeño profesional", hojas)
        hoja_6 = buscar_hoja("expectativas", hojas)
        hoja_7 = buscar_hoja("participación social", hojas)
        hoja_8 = buscar_hoja("comentarios", hojas)

        # Verifica que se encontraron todas
        print("Hojas encontradas:", list(hojas.keys()))


        errores = []
        procesadas = 0

        for idx, fila in hoja_s1.iterrows():
            curp = str(fila.get("CURP", "")).strip().lower()
            lapso = str(fila.get("Lapso(año y periodo (1 o 2) en el que se contestó la encuesta", "")).strip()
            if not curp:
                errores.append(f"Fila {idx+2}: CURP vacío")
                continue

            # Evitar duplicados de Encuesta
            if Encuesta.objects.filter(curp__curp=curp, lapso=lapso).exists():
                errores.append(f"Fila {idx+2}: Encuesta ya existe para {curp}–{lapso}")
                continue

            # Obtener o crear egresado fantasma
            egresado, _ = Egresado.objects.get_or_create(
                curp=curp,
                defaults={
                    'nombre': 'Pendiente',
                    'carrera': fila.get("Carrera de egreso", "No definida"),
                }
            )

            # Crear Encuesta
            encuesta = Encuesta.objects.create(
                curp=egresado,
                fechaInicio=date.today(),
                lapso=lapso,
                fechaFin=date.today()
            )

            try:
                # —————— S1 ——————
                if not EncuestaS1.objects.filter(folioEncuesta=encuesta).exists():
                    EncuestaS1.objects.create(
                        folioEncuesta=encuesta,
                        nombre=fila.get("Nombre"),
                        noControl=fila.get("No. de control"),
                        fechaNacimiento=convertir_fecha(fila.get("Fecha de Nacimiento")),
                        curp=curp,
                        sexo=map_sexo(fila.get("Sexo")),
                        estadoCivil=map_estado_civil(fila.get("Estado Civil")),
                        domicilio=fila.get("Domicilio"),
                        ciudad=fila.get("Ciudad"),
                        cp=fila.get("CP"),
                        email=fila.get("Email"),
                        telefono=fila.get("Teléfono"),
                        carrera=fila.get("Carrera de egreso"),
                        especialidad=fila.get("Especialidad"),
                        fechaEgreso=convertir_fecha(fila.get("Fecha de egreso")),
                        titulado=map_titulado(fila.get("Titulado(a)")),
                        dominioIngles=fila.get("Dominio del idioma inglés"),
                        otroIdioma=fila.get("Dominio del idioma inglés.1"),
                        manejoPaquetes=map_manejo_paquetes(fila.get("Manejo de paquetes computacionales")),
                        especificarPaquetes=fila.get("Manejo de paquetes computacionales.1")
                    )
                else:
                    errores.append(f"{curp}–{lapso}: S1 ya existe")

                # —————— S2 ——————
                f2 = hoja_s2.iloc[idx] if idx < len(hoja_s2) else {}
                if not EncuestaS2.objects.filter(folioEncuesta=encuesta).exists():
                    EncuestaS2.objects.create(
                        folioEncuesta=encuesta,
                        calidadDocentes=map_calificacion(f2.get("Calidad de los docentes")),
                        planEstudios=map_calificacion(f2.get("Plan de Estudios")),
                        oportunidadesProyectos=map_calificacion(f2.get("Oportunidad de participar en proyectos de investigación y desarrollo")),
                        enfasisInvestigacion=map_calificacion(f2.get("Énfasis en la investigación dentro del proceso de enseñanza")),
                        satisfaccionCondiciones=map_calificacion(f2.get("Satisfacción con las condiciones de estudio (infraestructura)")),
                        experienciaResidencia=map_calificacion(f2.get("Experiencia obtenida en la residencia profesional"))
                    )
                else:
                    errores.append(f"{curp}–{lapso}: S2 ya existe")

                # —————— S3 ——————
                f3 = hoja_s3.iloc[idx] if idx < len(hoja_s3) else {}
                if not EncuestaS3.objects.filter(folioEncuesta=encuesta).exists():
                    EncuestaS3.objects.create(
                        folioEncuesta=encuesta,
                        actividad=map_actividad(f3.get("¿Actividad actual?")),
                        tipoEstudio=map_tipo_estudio(f3.get("Si estudia, ¿qué tipo?")),
                        tipoEstudioOtro=f3.get("Otra:"),
                        especialidadInstitucion=f3.get("Especialidad e Institución:"),
                        tiempoObtenerEmpleo=map_tiempo_obtener_empleo(f3.get("Tiempo transcurrido para obtener el primer empleo")),
                        medioEmpleo=map_medio_empleo(f3.get("Medio para obtener el empleo")),
                        medioEmpleoOtro=f3.get("Otros:"),
                        requisitosContratacion=map_requisitos_contratacion(f3.get("Requisitos de contratación")),
                        requisitosContratacionOtro=f3.get("Otros.1"),
                        idiomaUtiliza=map_idioma_utiliza(f3.get("Idioma que utiliza en el trabajo")),
                        idiomaUtilizaOtro=f3.get("Otros.2"),
                        antiguedad=map_antiguedad(f3.get("Antigüedad en el empleo")),
                        anioIngreso=f3.get("Año de ingreso:"),
                        ingreso=map_ingreso(f3.get("Ingreso (salario mínimo diario)")),
                        nivelJerarquico=map_nivel_jerarquico(f3.get("Nivel jerárquico en el trabajo")),
                        condicionTrabajo=map_condicion_trabajo(f3.get("Condición de trabajo")),
                        condicionTrabajoOtro=f3.get("Otros.3"),
                        relacionTrabajo=map_relacion_trabajo(f3.get("Relación del trabajo con su área de formación"))
                    )
                else:
                    errores.append(f"{curp}–{lapso}: S3 ya existe")

                # ———— S3Empresa ————
                f3e = hoja_s3e.iloc[idx] if idx < len(hoja_s3e) else {}
                if not EncuestaS3Empresa.objects.filter(folioEncuesta=encuesta).exists():
                    EncuestaS3Empresa.objects.create(
                        folioEncuesta=encuesta,
                        tipoOrganismo=map_tipo_organismo(f3e.get("ORGANISMO")),
                        giroActividad=f3e.get("Giro o actividad"),
                        razonSocial=f3e.get("Razón social"),
                        domicilio=f3e.get("Domicilio"),
                        ciudad=f3e.get("Ciudad, Municipio, Estado"),
                        cp=f3e.get("CP empresa"),
                        email=f3e.get("E-mail"),
                        telefono=f3e.get("Teléfono"),
                        nombreJefeInmediato=f3e.get("Nombre y puesto del jefe inmediato"),  # ← viene junto
                        puestoJefeInmediato=None,  # ← opcional si no está separado en otra columna
                        sectorPrimario=map_sector_primario(f3e.get("Sector económico de la empresa: Sector primario")),
                        sectorSecundario=map_sector_secundario(f3e.get("Sector económico de la empresa: Sector secundario")),
                        sectorTerciario=map_sector_terciario(f3e.get("Sector económico de la empresa: Sector terciario")),
                        tamanoEmpresa=map_tamano_empresa(f3e.get("Tamaño de la empresa"))
                    )
                else:
                    errores.append(f"{curp}–{lapso}: S3Empresa ya existe")

                # —————— S4 ——————
                f4 = hoja_s4.iloc[idx] if idx < len(hoja_s4) else {}
                if not EncuestaS4.objects.filter(folioEncuesta=encuesta).exists():
                    EncuestaS4.objects.create(
                        folioEncuesta=encuesta,
                        eficiencia=map_eficiencia(f4.get("Eficiencia para realizar actividades laborales")),
                        formacion=map_formacion(f4.get("Formación académica vs desempeño laboral")),
                        utilidad=map_utilidad(f4.get("Utilidad de residencias o prácticas profesionales")),
                        areaCampoEstudio=map_valoracion(f4.get("Aspectos valorados por las empresas: Área o campo de estudio")),
                        titulacion=map_valoracion(f4.get("Aspectos valorados por las empresas: Titulación")),
                        experienciaLaboral=map_valoracion(f4.get("Aspectos valorados por las empresas: Experiencia laboral/práctica")),
                        competenciaLaboral=map_valoracion(f4.get("Aspectos valorados por las empresas: Competencia laboral")),
                        posicionamientoInstitucion=map_valoracion(f4.get("Aspectos valorados por las empresas: Posicionamiento de la institución")),
                        conocimientoIdiomas=map_valoracion(f4.get("Aspectos valorados por las empresas: Conocimiento de idiomas")),
                        recomendacionesReferencias=map_valoracion(f4.get("Aspectos valorados por las empresas: Recomendaciones/referencias")),
                        personalidadActitudes=map_valoracion(f4.get("Aspectos valorados por las empresas: Personalidad/actitudes")),
                        capacidadLiderazgo=map_valoracion(f4.get("Aspectos valorados por las empresas: Capacidad de liderazgo")),
                        otrosAspectos=map_valoracion(f4.get("Aspectos valorados por las empresas: Otros"))
                    )
                else:
                    errores.append(f"{curp}–{lapso}: S4 ya existe")

                # —————— S5 ——————
                if not EncuestaS5.objects.filter(folioEncuesta=encuesta).exists():
                    # Hoja 6
                    f6 = hoja_6.iloc[idx] if idx < len(hoja_6) else {}
                    # Hoja 7
                    f7 = hoja_7.iloc[idx] if idx < len(hoja_7) else {}
                    # Hoja 8
                    f8 = hoja_8.iloc[idx] if idx < len(hoja_8) else {}

                    EncuestaS5.objects.create(
                        folioEncuesta=encuesta,

                        # Hoja 6 – Actualización de conocimientos
                        cursosActualizacion=conv_si_no(f6.get("¿Le gustaría tomar cursos de actualización?")),
                        cursosActualizacionCuales=f6.get("¿Cuáles?"),
                        tomarPosgrado=conv_si_no(f6.get("¿Le gustaría tomar algún posgrado?")),
                        tomarPosgradoCual=f6.get("¿Cuáles?.1"),

                        # Hoja 7 – Participación social
                        perteneceOrganizacionesSociales=conv_si_no(f7.get("¿Pertenece a organizaciones sociales?")),
                        organizacionesSocialesCuales=f7.get("¿Cuáles?"),
                        perteneceOrganismosProfesionistas=conv_si_no(f7.get("¿Pertenece a organismos de profesionistas?")),
                        organismosProfesionistasCuales=f7.get("¿Cuáles?.1"),
                        perteneceAsociacionEgresados=conv_si_no(f7.get("¿Pertenece a la asociación de egresados?")),

                        # Hoja 8 – Comentarios y sugerencias
                        comentariosSugerencias=f8.get("Opiniones o recomendaciones para mejorar la formación profesional")
                    )

                else:
                    errores.append(f"{curp}–{lapso}: S5 ya existe")

                procesadas += 1

            except Exception as e:
                mensaje_error = f"{curp}–{lapso}: {str(e)}"
                errores.append(mensaje_error)
                print("❌ ERROR:", mensaje_error)

        
        if errores:
            print("Errores detectados:")
            for e in errores:
                print("-", e)

        return redirect('resumen_importaciones')

    return render(request, 'importar_encuesta.html')


def procesar_excel_anexo(request):
    
    if request.method != 'POST' or not request.FILES.get('archivo_excel'):
        return render(request, 'importar_anexo.html', {
            'errores': ["Debes seleccionar un archivo Excel para importar."]
        })
    else:
        hojas = pd.read_excel(request.FILES['archivo_excel'], sheet_name=None)
        print("Archivo recibido")
        h1 = hojas.get("DatosGenerales")
        h2 = hojas.get("SituaciónLaboral")
        h3 = hojas.get("Estudios-Institucion ")
        h4 = hojas.get("Desempeno")
        print("Hojas encontradas:", list(hojas.keys()))


        errores, procesadas = [], 0

        for idx, fila in h1.iterrows():
            curp = str(fila.get("Curp", "")).strip().lower()
            lapso = str(fila.get("Lapso(año y periodo (1 o 2) en el que se contestó la encuesta", "")).strip()
            if not curp or not lapso:
                errores.append(f"Fila {idx+2}: CURP o Lapso vacío")
                continue

            # Obtener o crear egresado fantasma
            egresado, _ = Egresado.objects.get_or_create(
                curp=curp,
                defaults={
                    'nombre': 'Pendiente',
                    'carrera': fila.get("Carrera", "No definida")
                }
            )

            # Evitar encuestas duplicadas
            if Encuesta.objects.filter(curp=egresado, lapso=lapso).exists():
                errores.append(f"Fila {idx+2}: Encuesta ya existe para {curp}–{lapso}")
                continue

            encuesta = Encuesta.objects.create(
                curp=egresado,
                fechaInicio=date.today(),
                lapso=lapso,
                fechaFin=date.today()
            )

            try:
                # --- AnexoS1 ---
                print("Procesando AnexoS1")
                if not AnexoS1.objects.filter(folioEncuesta=encuesta).exists():
                    titulacion_val = conv_si_no(fila.get("¿Estás titulado?"))
                    AnexoS1.objects.create(
                        folioEncuesta=encuesta,
                        nombreCompleto=fila.get("Nombre Completo"),
                        redesSociales=fila.get("Redes"),
                        fechaIngreso=convertir_fecha(fila.get("Fecha de Ingreso")),
                        telefono=fila.get("Telefono"),
                        correo=fila.get("Correo"),
                        fechaEgreso=convertir_fecha(fila.get("Fecha de Egreso")),
                        titulado=map_titulado(fila.get("¿Estás titulado?")),
                        razonNoTitulo=map_razon_no_titulo(fila.get("En caso de NO estar titulado, ¿cuál ha sido la razón?")) if titulacion_val == 0 else None,
                        razonNoTituloOtra=fila.get("razon otra")
                    )
                    print("AnexoS1 creado")
                else:
                    errores.append(f"{curp}–{lapso}: AnexoS1 ya existe")

                # --- AnexoS2 ---
                f2 = h2.iloc[idx] if idx < len(h2) else {}
                if not AnexoS2.objects.filter(folioEncuesta=encuesta).exists():
                    AnexoS2.objects.create(
                        folioEncuesta=encuesta,
                        trabaja=conv_si_no(f2.get("¿Trabajas Actualmente?")),
                        razonNoTrabaja=map_razon_no_trabaja(f2.get("En caso de que tu respuesta en la pregunta anterior sea NEGATIVA, señala la razón más importante:")),
                        razonNoTrabajaOtra=f2.get("Otra razón:"),
                        relacionTrabajoCarrera=conv_si_no(f2.get("¿Tu trabajo actual tiene relación con la carrera qué estudiaste?")),
                        antiguedad=map_antiguedad(f2.get("En caso de que sí trabajes, ¿cuál es la antigüedad de tu empleo actual?")),
                        tiempoTrabajoRelacionado=map_tiempo_trabajo_relacionado(f2.get("¿Después de egresar, en cuánto tiempo conseguiste trabajo relacionado con tu carrera?")),
                        razonNoConseguirTrabajo=f2.get("Si aún no lo consigues, ¿Cuál crees que sea la razón?"),
                        sector=map_sector(f2.get("Tipo de sector donde laboras:")),
                        sectorOtro=f2.get("Otro sector:"),
                        rol=map_rol(f2.get("¿Cuál es el rol que desempeñas en tu trabajo actual?")),
                        rolOtro=f2.get("Otro rol:"),
                        area=map_area(f2.get("Dentro de la empresa, ¿en qué área te desempeñas?")),
                        areaOtra=f2.get("Otra área:"),
                        medioTrabajo=map_medio_trabajo(f2.get("Medio principal para conseguir el primer trabajo después de egreso")),
                        medioTrabajoOtro=f2.get("Otro medio para conseguir empleo:"),
                        satisfaccion=map_satisfaccion(f2.get("Grado de satisfacción en tu trabajo actual"))
                    )
                else:
                    errores.append(f"{curp}–{lapso}: AnexoS2 ya existe")

                # --- AnexoS3 ---
                f3 = h3.iloc[idx] if idx < len(h3) else {}
                if not AnexoS3.objects.filter(folioEncuesta=encuesta).exists():
                    AnexoS3.objects.create(
                        folioEncuesta=encuesta,
                        competencias=map_competencias(f3.get("Acerca de las competencias adquiridas en la institución, ¿cómo consideras que te ayudan al desarrollo de tu trabajo?")),
                        satisfaccion=map_satisfaccion(f3.get("¿Cuál es el grado de satisfacción de la carrera que estudiaste?")),
                        educativo=map_educativo(f3.get("¿Qué sugieres reforzar y/o actualizar respecto a los contenidos del programa educativo?")),
                        educativoOtro=f3.get("Otro tema:"),
                        contacto=conv_si_no(f3.get("¿La Institución se ha contactado anteriormente contigo?")),
                        participar=conv_si_no(f3.get("¿Te gustaría participar con la Institución aportando tu experiencia profesional?")),
                        aporte=map_aporte(f3.get("¿Cómo podría ser tu participación?")),
                        aporteOtro=f3.get("Otra forma de participación:")
                    )
                else:
                    errores.append(f"{curp}–{lapso}: AnexoS3 ya existe")

                # --- AnexoS4 ---
                f4 = h4.iloc[idx] if idx < len(h4) else {}
                if not AnexoS4.objects.filter(folioEncuesta=encuesta).exists():
                    AnexoS4.objects.create(
                        folioEncuesta=encuesta,
                        herramientas=map_herramientas(f4.get("En tu desempeño laboral, ¿cuál(es) de las siguientes herramientas utilizas?")),
                        herramientasOtra=f4.get("Otras herramientas"),
                        colabora=conv_si_no(f4.get("¿Colaboras actualmente en proyectos de investigación y/o desarrollo?")),
                        tipoInvestigacion=map_tipo_investigacion(f4.get("En caso de ser POSITIVA la respuesta anterior, especifique el tipo de investigación y/o desarrollo")),
                        tipoInvestigacionOtra=f4.get("Especificar otras"),
                        participaRedes=conv_si_no(f4.get("¿Perteneces o participas en redes de colaboración?")),
                        certificacion=conv_si_no(f4.get("¿Cuentas con alguna certificación vigente nacional y/o internacional?")),
                        certificacionCuales=f4.get("En caso de que la respuesta anterior sea POSITIVA, menciónalas (respuesta abierta)"),
                        servicios=map_servicios(f4.get("¿Ofreces alguno de los siguientes servicios?")),
                        serviciosOtro=f4.get("Otros servicios"),
                        idiomas=map_idiomas(f4.get("¿Cuál de las siguientes lenguas extranjeras utilizas en tu actividad laboral?")),
                        idiomasOtro=f4.get("Otras lenguas"),
                        publicacion=conv_si_no(f4.get("¿Has realizado o colaborado con alguna publicación de un artículo en revista científica y/o de divulgación?")),
                        publicacionEspecifique=f4.get("En caso de que tu respuesta anterior haya sido POSITIVA, especifica (respuesta abierta)"),
                        documentos=map_documentos(f4.get("¿En cuál de los siguientes documentos has participado en su elaboración?")),
                        documentosOtro=f4.get("Otros documentos"),
                        calidad=map_calidad(f4.get("¿Qué sistema de gestión de calidad aplicas en tu actividad laboral?")),
                        calidadOtra=f4.get("Otro sistema"),
                        asociacion=conv_si_no(f4.get("¿Perteneces a alguna asociación profesional relacionada con tu carrera?")),
                        asociacionEspecifique=f4.get("En caso de que tu respuesta de la pregunta anterior sea POSITIVA, especifica a qué asociación perteneces (respuesta abierta)"),
                        etica=map_etica_anexo(f4.get("Desde tu punto de vista, el aporte de ética en un ambiente laboral consiste en:"))
                    )
                else:
                    errores.append(f"{curp}–{lapso}: AnexoS4 ya existe")

                procesadas += 1

            except Exception as e:
                errores.append(f"{curp}–{lapso}: Error → {str(e)}")
                traceback.print_exc()

        return redirect('resumen_importaciones')

    return redirect('importar_anexo')

