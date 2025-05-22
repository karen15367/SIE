import os
from django.shortcuts import render, redirect
from core.models import Egresado, Encuesta, EstadoEncuestaCarrera
from django.shortcuts import render, redirect
from core.models import AnexoS1, AnexoS2, AnexoS3, AnexoS4
from django.contrib import messages
from datetime import date
from datetime import datetime
from django.http import HttpResponse
from . import acuse


# Create your views here.

def calcular_lapso():
    hoy = date.today()
    año = hoy.year
    semestre = 1 if hoy.month <= 6 else 2
    return f"{año}-{semestre}"

def redirigir_anexo(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    egresado = Egresado.objects.filter(curp=curp).first()
    if not egresado:
        return redirect('index')
    
    estado = EstadoEncuestaCarrera.objects.filter(carrera__iexact=carrera).first()
    if estado and not estado.activa:
        messages.error(request, "La encuesta no está disponible para tu carrera en este momento.")
        return redirect('index')

    lapso_actual = calcular_lapso()
    encuesta = Encuesta.objects.filter(
        curp=egresado,
        lapso=lapso_actual,
        fechaFin__isnull=False
    ).first()

    if encuesta:
        return redirect('encuesta_finalizada')
    else:
        return redirect('anexo1')


def a1(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
            request.session['anexo_s1'] = {
                'nombre_completo': request.POST.get('nombre_completo'),
                'redes_sociales': request.POST.get('redes_sociales'),
                'fecha_ingreso': request.POST.get('fecha_ingreso'),
                'telefono': request.POST.get('telefono'),
                'correo': request.POST.get('email'),
                'fecha_egreso': request.POST.get('fechaEgreso'),
            }

            egresado = Egresado.objects.filter(curp=curp).first()
            if egresado:
                Encuesta.objects.get_or_create(
                    curp=egresado,
                    lapso=calcular_lapso(),
                    defaults={'fechaInicio': date.today()}
                )
            return redirect('anexo2')

        # Si es GET → precargar datos si ya hay versión anterior
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()

        # Encuesta actual
        encuesta_actual = Encuesta.objects.filter(curp=egresado, lapso=lapso_actual).first()

        # Encuesta anterior (con fechaFin ya respondida)
        encuesta_anterior = Encuesta.objects.filter(curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False).order_by('-lapso').first()

        if encuesta_anterior:
            anexo_anterior = AnexoS1.objects.filter(folioEncuesta=encuesta_anterior).first()
        else:
            anexo_anterior = None

        context = {}
        if anexo_anterior:
            context = {
                'nombre_completo': anexo_anterior.nombreCompleto,
                'redes_sociales': anexo_anterior.redesSociales,
                'fecha_ingreso': anexo_anterior.fechaIngreso,
                'telefono': anexo_anterior.telefono,
                'correo': anexo_anterior.correo,
                'fecha_egreso': anexo_anterior.fechaEgreso,
            }

        return render(request, 'Anexo1.html', context)

    except Exception as e:
        print("ERROR EN A1:", e)
        return redirect('index')


def a2(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            titulado = 1 if request.POST.get('titulado') == '1' else 0
            razon = request.POST.get('razonNoTitulo')
            razon_no_titulo = {'compromiso': 1, 'tiempo': 2, 'apoyo': 3, 'otro': 4}.get(razon, None)

            datos = request.session.get('anexo_s1', {})
            datos.update({
                'titulado': titulado,
                'razon_no_titulo': razon_no_titulo,
                'razon_no_titulo_otra': request.POST.get('razonNoTituloOtra', '') if razon_no_titulo == 4 else ''
            })

            encuesta = Encuesta.objects.filter(curp=curp).order_by('-folioEncuesta').first()
            if encuesta:
                AnexoS1.objects.update_or_create(
                    folioEncuesta=encuesta,
                    defaults={
                        'nombreCompleto': datos.get('nombre_completo'),
                        'redesSociales': datos.get('redes_sociales'),
                        'fechaIngreso': datos.get('fecha_ingreso'),
                        'telefono': datos.get('telefono'),
                        'correo': datos.get('correo'),
                        'fechaEgreso': datos.get('fecha_egreso'),
                        'titulado': datos.get('titulado'),
                        'razonNoTitulo': datos.get('razon_no_titulo'),
                        'razonNoTituloOtra': datos.get('razon_no_titulo_otra'),
                    }
                )
                request.session.pop('anexo_s1', None)
                return redirect('anexo3')
        except Exception as e:
            print("ERROR EN A2 (POST):", e)

    # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()
        encuesta_anterior = Encuesta.objects.filter(curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False).order_by('-lapso').first()
        anexo_anterior = AnexoS1.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'titulado': anexo_anterior.titulado,
                'razon_no_titulo': anexo_anterior.razonNoTitulo,
                'razon_no_titulo_otra': anexo_anterior.razonNoTituloOtra
            }

        return render(request, 'Anexo2.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A2:", e)

    return render(request, 'Anexo2.html')



def a3(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
            datos = {
                'trabaja': request.POST.get('trabaja'),
                'razon_no_trabaja': request.POST.get('razonNoTrabaja'),
                'razon_no_trabaja_otra': request.POST.get('razonNoTrabajaOtra', '')
            }

            request.session['anexo_s2'] = datos

            if datos['trabaja'] == '1':
                return redirect('anexo4')

            encuesta = Encuesta.objects.filter(curp=curp).order_by('-folioEncuesta').first()

            if encuesta:
                AnexoS2.objects.update_or_create(
                    folioEncuesta=encuesta,
                    defaults={
                        'trabaja': datos.get('trabaja'),
                        'razonNoTrabaja': datos.get('razon_no_trabaja'),
                        'razonNoTrabajaOtra': datos.get('razon_no_trabaja_otra')
                    }
                )
                request.session.pop('anexo_s2', None)
                return redirect('anexo7')

        # ⬇️ Este bloque es para GET (precarga)
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()

        encuesta_anterior = Encuesta.objects.filter(
            curp=egresado,
            lapso__lt=lapso_actual,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        if encuesta_anterior:
            anexo_anterior = AnexoS2.objects.filter(folioEncuesta=encuesta_anterior).first()
        else:
            anexo_anterior = None

        context = {}
        if anexo_anterior:
            context = {
                'trabaja': anexo_anterior.trabaja,
                'razon_no_trabaja': anexo_anterior.razonNoTrabaja,
                'razon_no_trabaja_otra': anexo_anterior.razonNoTrabajaOtra,
            }

        return render(request, 'Anexo3.html', context)

    except Exception as e:
        print("ERROR EN A3:", e)
        return render(request, 'Anexo3.html')


def a4(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            datos_previos = request.session.get('anexo_s2', {})

            datos_previos['relacion_trabajo_carrera'] = request.POST.get('relacionTrabajoCarrera')
            datos_previos['antiguedad'] = request.POST.get('antiguedad')
            datos_previos['tiempo_trabajo_relacionado'] = request.POST.get('tiempoTrabajoRelacionado')

            if request.POST.get('tiempoTrabajoRelacionado') == '4':
                datos_previos['razon_no_conseguir_trabajo'] = request.POST.get('razonNoConseguirTrabajo', '')

            request.session['anexo_s2'] = datos_previos
            return redirect('anexo5')
        except Exception as e:
            print("ERROR EN A4 (POST):", e)

    # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()
        encuesta_anterior = Encuesta.objects.filter(curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False).order_by('-lapso').first()
        anexo_anterior = AnexoS2.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'relacion_trabajo': anexo_anterior.relacionTrabajoCarrera,
                'antiguedad': anexo_anterior.antiguedad,
                'tiempo_trabajo_rel': anexo_anterior.tiempoTrabajoRelacionado,
                'razon_no_trabajo_rel': anexo_anterior.razonNoConseguirTrabajo,
            }

        return render(request, 'Anexo4.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A4:", e)

    return render(request, 'Anexo4.html')


def a5(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            datos_previos = request.session.get('anexo_s2', {})
            datos_previos['sector'] = request.POST.get('sector')
            if request.POST.get('sector') == '4':
                datos_previos['sector_otro'] = request.POST.get('sectorOtro', '')

            datos_previos['rol'] = request.POST.get('rol')
            if request.POST.get('rol') == '7':
                datos_previos['rol_otro'] = request.POST.get('rolOtro', '')

            datos_previos['area'] = request.POST.get('area')
            if request.POST.get('area') == '7':
                datos_previos['area_otra'] = request.POST.get('areaOtra', '')

            request.session['anexo_s2'] = datos_previos
            return redirect('anexo6')
        except Exception as e:
            print("ERROR EN A5 (POST):", e)

    # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()
        encuesta_anterior = Encuesta.objects.filter(curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False).order_by('-lapso').first()
        anexo_anterior = AnexoS2.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'sector': anexo_anterior.tipoSector,
                'sector_otro': anexo_anterior.tipoSectorOtro,
                'rol': anexo_anterior.rolTrabajo,
                'rol_otro': anexo_anterior.rolTrabajoOtro,
                'area': anexo_anterior.areaTrabajo,
                'area_otro': anexo_anterior.areaTrabajoOtra,
            }

        return render(request, 'Anexo5.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A5:", e)

    return render(request, 'Anexo5.html')


def a6(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
            datos = request.session.get('anexo_s2', {})
            datos.update({
                'medio_trabajo': request.POST.get('medioTrabajo'),
                'medio_trabajo_otro': request.POST.get('medioTrabajoOtro', '') if request.POST.get('medioTrabajo') == '5' else '',
                'satisfaccion': request.POST.get('satisfaccion')
            })

            encuesta = Encuesta.objects.filter(curp=curp).order_by('-folioEncuesta').first()

            if encuesta:
                AnexoS2.objects.update_or_create(
                    folioEncuesta=encuesta,
                    defaults={
                        'trabaja': datos.get('trabaja'),
                        'razonNoTrabaja': datos.get('razon_no_trabaja'),
                        'razonNoTrabajaOtra': datos.get('razon_no_trabaja_otra'),
                        'relacionTrabajoCarrera': datos.get('relacion_trabajo_carrera'),
                        'antiguedad': datos.get('antiguedad'),
                        'tiempoTrabajoRelacionado': datos.get('tiempo_trabajo_relacionado'),
                        'razonNoConseguirTrabajo': datos.get('razon_no_conseguir_trabajo'),
                        'sector': datos.get('sector'),
                        'sectorOtro': datos.get('sector_otro'),
                        'rol': datos.get('rol'),
                        'rolOtro': datos.get('rol_otro'),
                        'area': datos.get('area'),
                        'areaOtra': datos.get('area_otra'),
                        'medioTrabajo': datos.get('medio_trabajo'),
                        'medioTrabajoOtro': datos.get('medio_trabajo_otro'),
                        'satisfaccion': datos.get('satisfaccion'),
                    }
                )
                request.session.pop('anexo_s2', None)
                return redirect('anexo7')
    except Exception as e:
        print("ERROR EN A6:", e)
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()

        encuesta_anterior = Encuesta.objects.filter(
            curp=egresado,
            lapso__lt=lapso_actual,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        anexo_anterior = AnexoS2.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'medio_trabajo': anexo_anterior.medioTrabajo,
                'medio_trabajo_otro': anexo_anterior.medioTrabajoOtro,
                'satisfaccion': anexo_anterior.satisfaccion,
            }

        return render(request, 'Anexo6.html', context)

    except Exception as e:
        print("ERROR AL PRECARGAR A6:", e)

    return render(request, 'Anexo6.html')


def a7(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            request.session['anexo_s3'] = {
                'competencias': request.POST.get('competencias'),
                'satisfaccion': request.POST.get('satisfaccion'),
                'educativo': request.POST.get('educativo'),
                'educativo_otro': ''
            }

            if request.POST.get('educativo') == '5':
                request.session['anexo_s3']['educativo_otro'] = request.POST.get('educativoOtro', '')

            return redirect('anexo8')
        except Exception as e:
            print("ERROR EN A7 (POST):", e)

    # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()
        encuesta_anterior = Encuesta.objects.filter(curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False).order_by('-lapso').first()
        anexo_anterior = AnexoS3.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'competencias': anexo_anterior.competencias,
                'satisfaccion': anexo_anterior.satisfaccion,
                'educativo': anexo_anterior.educativo,
                'educativo_otro': anexo_anterior.educativoOtro,
            }

        return render(request, 'Anexo7.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A7:", e)

    return render(request, 'Anexo7.html')


def a8(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            datos = request.session.get('anexo_s3', {})
            datos.update({
                'contacto': request.POST.get('contacto'),
                'participar': request.POST.get('participar'),
                'aporte': request.POST.get('aporte'),
                'aporte_otro': request.POST.get('aporteOtro', '') if request.POST.get('aporte') in ['4', '7'] else ''
            })

            encuesta = Encuesta.objects.filter(curp=curp).order_by('-folioEncuesta').first()

            if encuesta:
                AnexoS3.objects.update_or_create(
                    folioEncuesta=encuesta,
                    defaults={
                        'competencias': datos.get('competencias'),
                        'satisfaccion': datos.get('satisfaccion'),
                        'educativo': datos.get('educativo'),
                        'educativoOtro': datos.get('educativo_otro'),
                        'contacto': datos.get('contacto'),
                        'participar': datos.get('participar'),
                        'aporte': datos.get('aporte'),
                        'aporteOtro': datos.get('aporte_otro'),
                    }
                )
                request.session.pop('anexo_s3', None)
                return redirect('anexo9')
        except Exception as e:
            print("ERROR EN A8:", e)

    # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()
        encuesta_anterior = Encuesta.objects.filter(curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False).order_by('-lapso').first()
        anexo_anterior = AnexoS3.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'contacto': anexo_anterior.contacto,
                'participar': anexo_anterior.participar,
                'aporte': anexo_anterior.aporte,
                'aporte_otro': anexo_anterior.aporteOtro,
            }

        return render(request, 'Anexo8.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A8:", e)

    return render(request, 'Anexo8.html')



def a9(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        # Iniciar recopilación de datos para AnexoS4
        request.session['anexo_s4'] = {
            'herramientas': request.POST.get('herramientas'),
            'herramientas_otra': '',
            'colabora': request.POST.get('colabora'),
            'tipo_investigacion': request.POST.get('tipoInvestigacion'),
            'tipo_investigacion_otra': ''
        }

        # Verificar si seleccionó "Otras" en herramientas y capturar el texto
        if request.POST.get('herramientas') == '5':
            request.session['anexo_s4']['herramientas_otra'] = request.POST.get(
                'herramientasOtra', '')

        # Verificar si seleccionó "Otras" en tipo_investigacion y capturar el texto
        if request.POST.get('tipoInvestigacion') == '5':
            request.session['anexo_s4']['tipo_investigacion_otra'] = request.POST.get(
                'tipoInvestigacionOtra', '')

        return redirect('anexo10')
        # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()
        encuesta_anterior = Encuesta.objects.filter(
            curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False
        ).order_by('-lapso').first()

        anexo_anterior = AnexoS4.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'herramientas': anexo_anterior.herramientas,
                'herramientas_otra': anexo_anterior.herramientasOtra,
                'colabora': anexo_anterior.colabora,
                'tipo_investigacion': anexo_anterior.tipoInvestigacion,
                'tipo_investigacion_otra': anexo_anterior.tipoInvestigacionOtra,
            }

        return render(request, 'Anexo9.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A9:", e)

    return render(request, 'Anexo9.html')



def a10(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            datos_previos = request.session.get('anexo_s4', {})

            datos_previos['participa_redes'] = request.POST.get('participaRedes')

            datos_previos['certificacion'] = request.POST.get('certificacion')
            datos_previos['certificacion_cuales'] = ''
            if request.POST.get('certificacion') == '1':
                datos_previos['certificacion_cuales'] = request.POST.get('certificacionCuales', '')

            datos_previos['servicios'] = request.POST.get('servicios')
            datos_previos['servicios_otro'] = ''
            if request.POST.get('servicios') == '5':
                datos_previos['servicios_otro'] = request.POST.get('serviciosOtro', '')

            datos_previos['idiomas'] = request.POST.get('idiomas')
            datos_previos['idiomas_otro'] = ''
            if request.POST.get('idiomas') == '5':
                datos_previos['idiomas_otro'] = request.POST.get('idiomasOtro', '')

            request.session['anexo_s4'] = datos_previos
            return redirect('anexo11')
        except Exception as e:
            print("ERROR EN A10 (POST):", e)

    # Precarga desde versiones anteriores (GET)
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()

        encuesta_anterior = Encuesta.objects.filter(
            curp=egresado,
            lapso__lt=lapso_actual,
            fechaFin__isnull=False
        ).order_by('-lapso').first()

        anexo_anterior = AnexoS4.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'participa_redes': anexo_anterior.participaRedes,
                'certificacion': anexo_anterior.certificacion,
                'certificacion_cuales': anexo_anterior.certificacionCuales,
                'servicios': anexo_anterior.servicios,
                'servicios_otro': anexo_anterior.serviciosOtro,
                'idiomas': anexo_anterior.idiomas,
                'idiomas_otro': anexo_anterior.idiomasOtro,
            }

        return render(request, 'Anexo10.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A10:", e)

    return render(request, 'Anexo10.html')



def a11(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            datos_previos = request.session.get('anexo_s4', {})

            datos_previos['publicacion'] = request.POST.get('publicacion')
            datos_previos['publicacion_especifique'] = ''
            if request.POST.get('publicacion') == '1':
                datos_previos['publicacion_especifique'] = request.POST.get('publicacionEspecifique', '')

            datos_previos['documentos'] = request.POST.get('documentos')
            datos_previos['documentos_otro'] = ''
            if request.POST.get('documentos') == '4':
                datos_previos['documentos_otro'] = request.POST.get('documentosOtro', '')

            datos_previos['calidad'] = request.POST.get('calidad')
            datos_previos['calidad_otra'] = ''
            if request.POST.get('calidad') == '3':
                datos_previos['calidad_otra'] = request.POST.get('calidadOtra', '')

            request.session['anexo_s4'] = datos_previos
            return redirect('anexo12')
        except Exception as e:
            print("ERROR EN A11 (POST):", e)

    # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()

        encuesta_anterior = Encuesta.objects.filter(
            curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False
        ).order_by('-lapso').first()

        anexo_anterior = AnexoS4.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'publicacion': anexo_anterior.publicacion,
                'publicacion_especifique': anexo_anterior.publicacionEspecifique,
                'documentos': anexo_anterior.documentos,
                'documentos_otro': anexo_anterior.documentosOtro,
                'calidad': anexo_anterior.calidad,
                'calidad_otra': anexo_anterior.calidadOtra,
            }

        return render(request, 'Anexo11.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A11:", e)

    return render(request, 'Anexo11.html')



def a12(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera or not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        try:
            datos = request.session.get('anexo_s4', {})
            datos.update({
                'asociacion': request.POST.get('asociacion'),
                'asociacion_especifique': request.POST.get('asociacionEspecifique', '') if request.POST.get('asociacion') == '1' else '',
                'etica': request.POST.get('etica')
            })

            encuesta = Encuesta.objects.filter(curp=curp).order_by('-folioEncuesta').first()

            if encuesta:
                AnexoS4.objects.update_or_create(
                    folioEncuesta=encuesta,
                    defaults={
                        'herramientas': datos.get('herramientas'),
                        'herramientasOtra': datos.get('herramientas_otra'),
                        'colabora': datos.get('colabora'),
                        'tipoInvestigacion': datos.get('tipo_investigacion'),
                        'tipoInvestigacionOtra': datos.get('tipo_investigacion_otra'),
                        'participaRedes': datos.get('participa_redes'),
                        'certificacion': datos.get('certificacion'),
                        'certificacionCuales': datos.get('certificacion_cuales'),
                        'servicios': datos.get('servicios'),
                        'serviciosOtro': datos.get('servicios_otro'),
                        'idiomas': datos.get('idiomas'),
                        'idiomasOtro': datos.get('idiomas_otro'),
                        'publicacion': datos.get('publicacion'),
                        'publicacionEspecifique': datos.get('publicacion_especifique'),
                        'documentos': datos.get('documentos'),
                        'documentosOtro': datos.get('documentos_otro'),
                        'calidad': datos.get('calidad'),
                        'calidadOtra': datos.get('calidad_otra'),
                        'asociacion': datos.get('asociacion'),
                        'asociacionEspecifique': datos.get('asociacion_especifique'),
                        'etica': datos.get('etica'),
                    }
                )
                encuesta.fechaFin = date.today()
                encuesta.save()
                request.session.pop('anexo_s4', None)
                return redirect('encuesta_finalizada')
        except Exception as e:
            print("ERROR EN A12 (POST):", e)

    # Precarga para GET
    try:
        egresado = Egresado.objects.filter(curp=curp).first()
        lapso_actual = calcular_lapso()

        encuesta_anterior = Encuesta.objects.filter(
            curp=egresado, lapso__lt=lapso_actual, fechaFin__isnull=False
        ).order_by('-lapso').first()

        anexo_anterior = AnexoS4.objects.filter(folioEncuesta=encuesta_anterior).first() if encuesta_anterior else None

        context = {}
        if anexo_anterior:
            context = {
                'asociacion': anexo_anterior.asociacion,
                'asociacion_especifique': anexo_anterior.asociacionEspecifique,
                'etica': anexo_anterior.etica,
            }

        return render(request, 'Anexo12.html', context)
    except Exception as e:
        print("ERROR AL PRECARGAR A12:", e)

    return render(request, 'Anexo12.html')



def encuesta_finalizada(request):
    curp = request.session.get('usuario_id')
    if not curp:
        return redirect('index')

    # Obtener encuesta activa
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
    fecha_final = encuesta.fechaFin.strftime('%d de %B de %Y') if encuesta.fechaFin else "pendiente"
    hora = encuesta.fechaFin.strftime('%H:%M:%S') if encuesta.fechaFin else "pendiente"
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
    bytesMap= acuse.generate_document(return_bytes=True,variables= vars)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="acuse.pdf"'

    response.write(bytesMap.getvalue())

    return response
