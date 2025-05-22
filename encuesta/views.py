import os
from django.shortcuts import render, redirect
from datetime import date
from django.contrib import messages
import datetime
from django.http import HttpResponse
from . import acuse
from core.models import (
    Encuesta, EncuestaS1, EncuestaS2, EncuestaS3, EncuestaS3Empresa,
    EncuestaS4, EncuestaS5, Egresado, EstadoEncuestaCarrera
)


def calcular_lapso():
    hoy = date.today()
    año = hoy.year
    semestre = 1 if hoy.month <= 6 else 2
    return f"{año}-{semestre}"

def redirigir_encuesta(request):
    curp = request.session.get('usuario_id')
    if not curp:
        return redirect('index')

    egresado = Egresado.objects.filter(curp=curp).first()
    if not egresado:
        return redirect('index')
    
    carrera = egresado.carrera
    estado = EstadoEncuestaCarrera.objects.filter(carrera__iexact=carrera).first()
    if estado and not estado.activa:
        messages.error(request, "La encuesta no está disponible para tu carrera en este momento.")
        return redirect('index')

    lapso_actual = calcular_lapso()
    encuesta = Encuesta.objects.filter(curp=egresado, lapso=lapso_actual, fechaFin__isnull=False).first()

    if encuesta:
        return redirect('encuesta_finalizada')  # Ya la respondió
    else:
        return redirect('e1')  # Comienza desde la encuesta1


def e1(request):
    curp = request.session.get('usuario_id')
    if not curp:
        return redirect('index')

    if request.method == 'POST':
        egresado = Egresado.objects.filter(curp=curp).first()
        encuesta, _ = Encuesta.objects.get_or_create(
            curp=egresado,
            lapso=calcular_lapso(),
            defaults={'fechaInicio': date.today()}
        )
        request.session['folio_encuesta'] = encuesta.folioEncuesta

        request.session['encuesta_s1'] = {
            'nombre': request.POST.get('nombre'),
            'noControl': request.POST.get('noControl'),
            'fechaNacimiento': request.POST.get('fechaNacimiento'),
            'curp': request.POST.get('curp'),
            'sexo': request.POST.get('sexo'),
            'estadoCivil': request.POST.get('estadoCivil'),
            'domicilio': request.POST.get('domicilio'),
            'ciudad': request.POST.get('ciudad'),
            'cp': request.POST.get('cp'),
            'email': request.POST.get('email'),
            'telefono': request.POST.get('telefono'),
        }
        return redirect('e2')

    # Precarga desde encuesta anterior
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()
        encuesta_anterior = Encuesta.objects.filter(
            curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s1 = EncuestaS1.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s1:
            context = {
                'nombre': encuesta_s1.nombre,
                'noControl': encuesta_s1.noControl,
                'fechaNacimiento': encuesta_s1.fechaNacimiento,
                'curp': encuesta_s1.curp,
                'sexo': encuesta_s1.sexo,
                'estadoCivil': encuesta_s1.estadoCivil,
                'domicilio': encuesta_s1.domicilio,
                'ciudad': encuesta_s1.ciudad,
                'cp': encuesta_s1.cp,
                'email': encuesta_s1.email,
                'telefono': encuesta_s1.telefono,
            }

        return render(request, 'encuesta1.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E1:", e)

    return render(request, 'encuesta1.html')


def e2(request):
    if request.method == 'POST':
        datos = request.session.get('encuesta_s1', {})
        fi = request.POST.get('fechaingreso')
        fe = request.POST.get('fechaEgreso')
        datos.update({
            'carrera': request.POST.get('carrera'),
            'especialidad': request.POST.get('Especialidad'),
            'fechaIngreso': datetime.datetime.strptime(
                fi, '%Y-%m-%d').date(),
            'fechaEgreso': datetime.datetime.strptime(
                fe, '%Y-%m-%d').date(),
            'titulado': request.POST.get('titulo'),
            'dominioIngles': request.POST.get('dominio'),
            'otroIdioma': request.POST.get('idioma'),
            'manejoPaquetes': request.POST.get('paquetes'),
            'especificarPaquetes': request.POST.get('paquetesE')
        })

        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        EncuestaS1.objects.update_or_create(
            folioEncuesta=encuesta,
            defaults=datos
        )

        request.session.pop('encuesta_s1', None)
        return redirect('e3')
        # Precarga para GET
    try:
        folio = request.session.get('folio_encuesta')
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp, lapso__lt=encuesta.lapso, fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s1 = EncuestaS1.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s1:
            context = {
                'carrera': encuesta_s1.carrera,
                'especialidad': encuesta_s1.especialidad,
                'fechaIngreso': encuesta_s1.fechaIngreso,
                'fechaEgreso': encuesta_s1.fechaEgreso,
                'titulado': encuesta_s1.titulado,
                'dominio': encuesta_s1.dominioIngles,
                'idioma': encuesta_s1.otroIdioma,
                'paquetes': encuesta_s1.manejoPaquetes,
                'paquetesE': encuesta_s1.especificarPaquetes,
            }

        return render(request, 'encuesta2.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E2:", e)

    return render(request, 'encuesta2.html')


def e3(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        EncuestaS2.objects.update_or_create(
            folioEncuesta=encuesta,
            defaults={
                'calidadDocentes': request.POST.get('calidadDocentes'),
                'planEstudios': request.POST.get('planEstudios'),
                'oportunidadesProyectos': request.POST.get('oportunidadesProyectos'),
                'enfasisInvestigacion': request.POST.get('enfasisInvestigacion'),
                'satisfaccionCondiciones': request.POST.get('satisfaccionCondiciones'),
                'experienciaResidencia': request.POST.get('experienciaResidencia')
            }
        )
        return redirect('e4')

    # Precarga desde versiones anteriores
    try:
        folio = request.session.get('folio_encuesta')
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp,
            lapso__lt=encuesta.lapso,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s2 = EncuestaS2.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s2:
            context = {
                'calidadDocentes': encuesta_s2.calidadDocentes,
                'planEstudios': encuesta_s2.planEstudios,
                'oportunidadesProyectos': encuesta_s2.oportunidadesProyectos,
                'enfasisInvestigacion': encuesta_s2.enfasisInvestigacion,
                'satisfaccionCondiciones': encuesta_s2.satisfaccionCondiciones,
                'experienciaResidencia': encuesta_s2.experienciaResidencia,
            }

        return render(request, 'encuesta3.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E3:", e)

    return render(request, 'encuesta3.html')


def e4(request):
    if request.method == 'POST':
        try:
            actividad = int(request.POST.get('actividad'))
            datos = {
                'actividad': actividad,
                'tipoEstudio': request.POST.get('tipoEstudio'),
                'tipoEstudioOtro': request.POST.get('tipoEstudioOtro'),
                'especialidadInstitucion': request.POST.get('especialidadInstitucion'),
                'tiempoObtenerEmpleo': request.POST.get('tiempoObtenerEmpleo')
            }

            folio = request.session['folio_encuesta']
            encuesta = Encuesta.objects.get(folioEncuesta=folio)

            EncuestaS3.objects.update_or_create(
                folioEncuesta=encuesta,
                defaults=datos
            )

            return redirect('e9') if actividad in [2, 4] else redirect('e5')
        except Exception as e:
            print("ERROR EN E4 (POST):", e)

    # Precarga desde versiones anteriores
    try:
        folio = request.session.get('folio_encuesta')
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp,
            lapso__lt=encuesta.lapso,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s3 = EncuestaS3.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s3:
            context = {
                'actividad': encuesta_s3.actividad,
                'tipoEstudio': encuesta_s3.tipoEstudio,
                'tipoEstudioOtro': encuesta_s3.tipoEstudioOtro,
                'especialidadInstitucion': encuesta_s3.especialidadInstitucion,
                'tiempoObtenerEmpleo': encuesta_s3.tiempoObtenerEmpleo,
            }

        return render(request, 'encuesta4.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E4:", e)

    return render(request, 'encuesta4.html')



def e5(request):
    if request.method == 'POST':
        try:
            datos = {
                'medioEmpleo': request.POST.get('medioEmpleo'),
                'medioEmpleoOtro': request.POST.get('medioEmpleoOtro', '') if request.POST.get('medioEmpleo') == '5' else '',
                'requisitosContratacion': request.POST.get('requisitosContratacion'),
                'requisitosContratacionOtro': request.POST.get('requisitosContratacionOtro', '') if request.POST.get('requisitosContratacion') == '7' else '',
                'idiomaUtiliza': request.POST.get('idiomaUtiliza'),
                'idiomaUtilizaOtro': request.POST.get('idiomaUtilizaOtro', '') if request.POST.get('idiomaUtiliza') == '5' else '',
                'hablarPorcentaje': request.POST.get('hablarPorcentaje'),
                'escribirPorcentaje': request.POST.get('escribirPorcentaje'),
                'leerPorcentaje': request.POST.get('leerPorcentaje'),
                'escucharPorcentaje': request.POST.get('escucharPorcentaje'),
            }

            folio = request.session['folio_encuesta']
            encuesta = Encuesta.objects.get(folioEncuesta=folio)

            EncuestaS3.objects.update_or_create(
                folioEncuesta=encuesta,
                defaults=datos
            )
            return redirect('e6')
        except Exception as e:
            print("ERROR EN E5 (POST):", e)

    # Precarga desde versiones anteriores
    try:
        folio = request.session.get('folio_encuesta')
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp,
            lapso__lt=encuesta.lapso,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s3 = EncuestaS3.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s3:
            context = {
                'medioEmpleo': encuesta_s3.medioEmpleo,
                'medioEmpleoOtro': encuesta_s3.medioEmpleoOtro,
                'requisitosContratacion': encuesta_s3.requisitosContratacion,
                'requisitosContratacionOtro': encuesta_s3.requisitosContratacionOtro,
                'idiomaUtiliza': encuesta_s3.idiomaUtiliza,
                'idiomaUtilizaOtro': encuesta_s3.idiomaUtilizaOtro,
                'hablarPorcentaje': encuesta_s3.hablarPorcentaje,
                'escribirPorcentaje': encuesta_s3.escribirPorcentaje,
                'leerPorcentaje': encuesta_s3.leerPorcentaje,
                'escucharPorcentaje': encuesta_s3.escucharPorcentaje,
            }

        return render(request, 'encuesta5.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E5:", e)

    return render(request, 'encuesta5.html')



def e6(request):
    if request.method == 'POST':
        try:
            folio = request.session['folio_encuesta']
            encuesta = Encuesta.objects.get(folioEncuesta=folio)
            EncuestaS3.objects.filter(folioEncuesta=encuesta).update(
                antiguedad=request.POST.get('antiguedad'),
                anioIngreso=request.POST.get('anioIngreso'),
                ingreso=request.POST.get('ingreso'),
                nivelJerarquico=request.POST.get('nivelJerarquico'),
                condicionTrabajo=request.POST.get('condicionTrabajo'),
                condicionTrabajoOtro=request.POST.get('condicionTrabajoOtro'),
                relacionTrabajo=request.POST.get('relacionTrabajo')
            )
            return redirect('e7')
        except Exception as e:
            print("ERROR EN E6 (POST):", e)

    # Precarga desde encuesta anterior
    try:
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp,
            lapso__lt=encuesta.lapso,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s3 = EncuestaS3.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s3:
            context = {
                'antiguedad': encuesta_s3.antiguedad,
                'anioIngreso': encuesta_s3.anioIngreso,
                'ingreso': encuesta_s3.ingreso,
                'nivelJerarquico': encuesta_s3.nivelJerarquico,
                'condicionTrabajo': encuesta_s3.condicionTrabajo,
                'condicionTrabajoOtro': encuesta_s3.condicionTrabajoOtro,
                'relacionTrabajo': encuesta_s3.relacionTrabajo,
            }

        return render(request, 'encuesta6.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E6:", e)

    return render(request, 'encuesta6.html')



def e7(request):
    if request.method == 'POST':
        request.session['empresa'] = {
            'tipoOrganismo': request.POST.get('tipoOrganismo'),
            'giroActividad': request.POST.get('giroActividad'),
            'razonSocial': request.POST.get('razonSocial'),
            'domicilio': request.POST.get('domicilio'),
            'ciudad': request.POST.get('ciudad'),
            'cp': request.POST.get('cp'),
            'email': request.POST.get('email'),
            'telefono': request.POST.get('telefono'),
            'nombreJefeInmediato': request.POST.get('nombreJefeInmediato'),
            'puestoJefeInmediato': request.POST.get('puestoJefeInmediato')
        }
        return redirect('e8')

    # Precargar desde versión anterior
    try:
        folio = request.session.get('folio_encuesta')
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp,
            lapso__lt=encuesta.lapso,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        empresa_ant = EncuestaS3Empresa.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if empresa_ant:
            context = {
                'tipoOrganismo': empresa_ant.tipoOrganismo,
                'giroActividad': empresa_ant.giroActividad,
                'razonSocial': empresa_ant.razonSocial,
                'domicilio': empresa_ant.domicilio,
                'ciudad': empresa_ant.ciudad,
                'cp': empresa_ant.cp,
                'email': empresa_ant.email,
                'telefono': empresa_ant.telefono,
                'nombreJefeInmediato': empresa_ant.nombreJefeInmediato,
                'puestoJefeInmediato': empresa_ant.puestoJefeInmediato,
            }

        return render(request, 'encuesta7.html', context)
    except Exception as e:
        print("ERROR EN PRECARGA E7:", e)

    return render(request, 'encuesta7.html')



def e8(request):
    if request.method == 'POST':
        datos = request.session.get('empresa', {})
        datos.update({
            'sectorPrimario': request.POST.get('sectorPrimario'),
            'sectorSecundario': request.POST.get('sectorSecundario'),
            'sectorTerciario': request.POST.get('sectorTerciario'),
            'tamanoEmpresa': request.POST.get('tamanoEmpresa')
        })
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        EncuestaS3Empresa.objects.update_or_create(
            folioEncuesta=encuesta,
            defaults=datos
        )

        request.session.pop('empresa', None)
        return redirect('e9')

    # Precarga desde versión anterior
    try:
        folio = request.session.get('folio_encuesta')
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp,
            lapso__lt=encuesta.lapso,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        empresa_ant = EncuestaS3Empresa.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if empresa_ant:
            context = {
                'sectorPrimario': empresa_ant.sectorPrimario,
                'sectorSecundario': empresa_ant.sectorSecundario,
                'sectorTerciario': empresa_ant.sectorTerciario,
                'tamanoEmpresa': empresa_ant.tamanoEmpresa,
            }

        return render(request, 'encuesta8.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E8:", e)

    return render(request, 'encuesta8.html')



def e9(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        EncuestaS4.objects.update_or_create(
            folioEncuesta=encuesta,
            defaults={
                'eficiencia': request.POST.get('eficiencia'),
                'formacion': request.POST.get('formacion'),
                'utilidad': request.POST.get('utilidad'),
            }
        )
        return redirect('e10')

    try:
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp, lapso__lt=encuesta.lapso, fechaFin__isnull=False
        ).order_by('-lapso').first()
        encuesta_s4 = EncuestaS4.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s4:
            context = {
                'eficiencia': encuesta_s4.eficiencia,
                'formacion': encuesta_s4.formacion,
                'utilidad': encuesta_s4.utilidad,
            }

        return render(request, 'encuesta9.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E9:", e)

    return render(request, 'encuesta9.html')



def e10(request):
    if request.method == 'POST':
        try:
            folio = request.session['folio_encuesta']
            encuesta = Encuesta.objects.get(folioEncuesta=folio)

            EncuestaS4.objects.filter(folioEncuesta=encuesta).update(
                areaCampoEstudio=request.POST.get('aspecto1'),
                titulacion=request.POST.get('aspecto2'),
                experienciaLaboral=request.POST.get('aspecto3'),
                competenciaLaboral=request.POST.get('aspecto4'),
                posicionamientoInstitucion=request.POST.get('aspecto5'),
                conocimientoIdiomas=request.POST.get('aspecto6'),
                recomendacionesReferencias=request.POST.get('aspecto7'),
                personalidadActitudes=request.POST.get('aspecto8'),
                capacidadLiderazgo=request.POST.get('aspecto9'),
                otrosAspectos=request.POST.get('aspecto10')
            )
            return redirect('e11')
        except Exception as e:
            print("ERROR EN E10 (POST):", e)

    # Precarga desde encuesta anterior
    try:
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp, lapso__lt=encuesta.lapso, fechaFin__isnull=False
        ).order_by('-lapso').first()
        encuesta_s4 = EncuestaS4.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s4:
            context = {
                'aspecto1': encuesta_s4.areaCampoEstudio,
                'aspecto2': encuesta_s4.titulacion,
                'aspecto3': encuesta_s4.experienciaLaboral,
                'aspecto4': encuesta_s4.competenciaLaboral,
                'aspecto5': encuesta_s4.posicionamientoInstitucion,
                'aspecto6': encuesta_s4.conocimientoIdiomas,
                'aspecto7': encuesta_s4.recomendacionesReferencias,
                'aspecto8': encuesta_s4.personalidadActitudes,
                'aspecto9': encuesta_s4.capacidadLiderazgo,
                'aspecto10': encuesta_s4.otrosAspectos,
            }

        return render(request, 'encuesta10.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E10:", e)

    return render(request, 'encuesta10.html')




def e11(request):
    if request.method == 'POST':
        request.session['s5'] = {
            'cursosActualizacion': request.POST.get('cursos'),
            'cursosActualizacionCuales': request.POST.get('cursosCual'),
            'tomarPosgrado': request.POST.get('posgrado'),
            'tomarPosgradoCual': request.POST.get('posgradoCual'),
            'perteneceOrganizacionesSociales': request.POST.get('organizaciones'),
            'organizacionesSocialesCuales': request.POST.get('organizacionesCual'),
            'perteneceOrganismosProfesionistas': request.POST.get('profesionistas'),
            'organismosProfesionistasCuales': request.POST.get('profesionistasCual'),
            'perteneceAsociacionEgresados': request.POST.get('egresados')
        }
        return redirect('e12')

    # Precarga desde versión anterior
    try:
        folio = request.session.get('folio_encuesta')
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp, lapso__lt=encuesta.lapso, fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s5 = EncuestaS5.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s5:
            context = {
                'cursos': encuesta_s5.cursosActualizacion,
                'cursosCual': encuesta_s5.cursosActualizacionCuales,
                'posgrado': encuesta_s5.tomarPosgrado,
                'posgradoCual': encuesta_s5.tomarPosgradoCual,
                'organizaciones': encuesta_s5.perteneceOrganizacionesSociales,
                'organizacionesCual': encuesta_s5.organizacionesSocialesCuales,
                'profesionistas': encuesta_s5.perteneceOrganismosProfesionistas,
                'profesionistasCual': encuesta_s5.organismosProfesionistasCuales,
                'egresados': encuesta_s5.perteneceAsociacionEgresados,
            }

        return render(request, 'encuesta11.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E11:", e)

    return render(request, 'encuesta11.html')



def e12(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        datos = request.session.get('s5', {})

        datos['comentariosSugerencias'] = request.POST.get('comentariosSugerencias')

        EncuestaS5.objects.update_or_create(
            folioEncuesta=encuesta,
            defaults=datos
        )

        encuesta.fechaFin = date.today()
        encuesta.save()
        request.session.pop('s5', None)
        return redirect('encuesta_finalizada')

    # Precarga desde versión anterior
    try:
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)

        encuesta_anterior = Encuesta.objects.filter(
            curp=encuesta.curp, lapso__lt=encuesta.lapso, fechaFin__isnull=False
        ).order_by('-lapso').first()

        encuesta_s5 = EncuestaS5.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if encuesta_s5:
            context['comentariosSugerencias'] = encuesta_s5.comentariosSugerencias

        return render(request, 'encuesta12.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR E12:", e)

    return render(request, 'encuesta12.html')

def encuesta_finalizada(request):
    curp = request.session.get('usuario_id')
    if not curp:
        return redirect('index')

    egresado = Egresado.objects.filter(curp=curp).first()
    encuesta = Encuesta.objects.filter(
        curp=egresado).order_by('-folioEncuesta').first()

    if encuesta:
        encuesta.fechaFin = date.today()
        encuesta.save()
        lapso = encuesta.lapso
    else:
        lapso = calcular_lapso()

    return render(request, 'encuestaFinalizada.html', {
        'lapso': lapso
    })


def generar_acuse_pdf(request):
    curp = request.session.get('usuario_id')
    if not curp:
        return redirect('index')

    egresado = Egresado.objects.filter(curp=curp).first()
    encuesta = Encuesta.objects.filter(
        curp=egresado).order_by('-folioEncuesta').first()

    if not egresado or not encuesta:
        return redirect('index')

    nombre = egresado.nombre
    fecha_final = encuesta.fechaFin.strftime(
        '%d de %B de %Y') if encuesta.fechaFin else "pendiente"
    hora = encuesta.fechaFin.strftime(
        '%H:%M:%S') if encuesta.fechaFin else "pendiente"
    lapso = encuesta.lapso
    cadena = f"{curp}|{nombre}|{fecha_final}|{hora}"

    IMAGES_DIR = "templates/static/img"
    vars = {
        'nombre': f'{nombre}',
        'dependencia': 'ANEXO Quím y bio Quím.',
        'expediente':  f'{egresado.noControl}',
        'content': (
            f"Perteneciente a la carrera de <b>{egresado.carrera}</b> realizó el anexo "
            f"perteneciente a la carrera de Quím y Bio Quím el día <b>{fecha_final}</b> "
            f"en la hora marcada como <b>{hora}</b> correspondiente al periodo <b>{lapso}</b>. "
            "Por tal motivo sus registros correspondientes a sus datos personales han quedado registrados satisfactoriamente."
        ),
        'cadena_digital': f'{cadena}',
        'signature': 'Nombre y firma autorizada',
        'direccion': (
            "Calz. Miguel Ángel de Quevedo 2779, Col. Formando Hogar. C.P. 91897 H. Veracruz, Ver. Tel. (229) 934 15 00 · https://www.veracruz.tecnm.mx"
        ),
        'logo_sep_path': os.path.join(IMAGES_DIR, 'sepB.png'),
        'logo_footer_path': os.path.join(IMAGES_DIR, 'logo.png'),
        'watermark_path': os.path.join(IMAGES_DIR, 'uemex.jpg')
    }

    # Verificar existencia de imágenes
    for key in ['logo_sep_path', 'logo_footer_path', 'watermark_path']:
        if not os.path.exists(vars[key]):
            print(f"Advertencia: no se encontró {vars[key]}")

    # Ejemplo de uso para guardar en un archivo
    bytesMap = acuse.generate_document(return_bytes=True, variables=vars)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="acuse.pdf"'

    response.write(bytesMap.getvalue())

    return response
