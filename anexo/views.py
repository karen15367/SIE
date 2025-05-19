import os
from django.shortcuts import render, redirect
from core.models import Egresado, Encuesta
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
                'correo': request.POST.get('correo'),
                'fecha_egreso': request.POST.get('fecha_egreso'),
            }

            egresado = Egresado.objects.filter(curp=curp).first()
            if egresado:
                Encuesta.objects.get_or_create(
                    curp=egresado,
                    lapso=calcular_lapso(),
                    defaults={'fechaInicio': date.today()}
                )
            return redirect('anexo2')
    except Exception as e:
        print("ERROR EN A1:", e)

    return render(request, 'Anexo1.html')


def a2(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
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
        print("ERROR EN A2:", e)

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
    except Exception as e:
        print("ERROR EN A3:", e)

    return render(request, 'Anexo3.html')


def a4(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
            # Recuperar datos previos
            datos_previos = request.session.get('anexo_s2', {})

            # Añadir nuevos datos
            datos_previos['relacion_trabajo_carrera'] = request.POST.get(
                'trabaja')  # Nota: mismo nombre en el HTML
            datos_previos['antiguedad'] = request.POST.get('antiguedad')
            datos_previos['tiempo_trabajo_relacionado'] = request.POST.get(
                'tiempoTrabajoRelacionado')

            # Verificar si seleccionó "Aún no lo consigo" y capturar el motivo
            if request.POST.get('tiempoTrabajoRelacionado') == '4':
                datos_previos['razon_no_conseguir_trabajo'] = request.POST.get(
                    'razonNoConseguirTrabajo', '')

            # Actualizar sesión
            request.session['anexo_s2'] = datos_previos

            return redirect('anexo5')
    except Exception as e:
        print("Error:", e)

    return render(request, 'Anexo4.html')


def a5(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
            # Recuperar datos previos
            datos_previos = request.session.get('anexo_s2', {})

            # Añadir nuevos datos
            datos_previos['sector'] = request.POST.get('sector')
            # Verificar si seleccionó "Otro" sector y capturar el texto
            if request.POST.get('sector') == '4':
                datos_previos['sector_otro'] = request.POST.get(
                    'sectorOtro', '')

            datos_previos['rol'] = request.POST.get('rol')
            # Verificar si seleccionó "Otras" en rol y capturar el texto
            if request.POST.get('rol') == '7':
                datos_previos['rol_otro'] = request.POST.get('rolOtro', '')

            datos_previos['area'] = request.POST.get('area')
            # Verificar si seleccionó "Otras" en área y capturar el texto
            if request.POST.get('area') == '7':
                datos_previos['area_otra'] = request.POST.get('areaOtra', '')

            # Actualizar sesión
            request.session['anexo_s2'] = datos_previos

            return redirect('anexo6')
    except Exception as e:
        print("Error:", e)

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

    return render(request, 'Anexo6.html')


def a7(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
            # Iniciar recopilación de datos para AnexoS3
            request.session['anexo_s3'] = {
                'competencias': request.POST.get('competencias'),
                'satisfaccion': request.POST.get('satisfaccion'),
                'educativo': request.POST.get('educativo'),
                'educativo_otro': ''
            }

            # Verificar si seleccionó "Otras" y capturar el texto
            if request.POST.get('educativo') == '5':
                request.session['anexo_s3']['educativo_otro'] = request.POST.get(
                    'educativoOtro', '')

            return redirect('anexo8')
    except Exception as e:
        print("Error:", e)

    return render(request, 'Anexo7.html')


def a8(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    try:
        if request.method == 'POST':
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

    return render(request, 'Anexo9.html')


def a10(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        # Recuperar datos previos
        datos_previos = request.session.get('anexo_s4', {})

        # Añadir nuevos datos
        datos_previos['participa_redes'] = request.POST.get(
            'trabaja')  # Parece haber un error en el nombre del campo
        datos_previos['certificacion'] = request.POST.get('certificacion')
        datos_previos['certificacion_cuales'] = ''

        # Verificar si seleccionó "Si" en certificacion y capturar el texto
        if request.POST.get('certificacion') == '1':
            datos_previos['certificacion_cuales'] = request.POST.get(
                'certificacionCuales', '')

        datos_previos['servicios'] = request.POST.get('servicios')
        datos_previos['servicios_otro'] = ''

        # Verificar si seleccionó "Otras" en servicios y capturar el texto
        if request.POST.get('servicios') == '5':
            datos_previos['servicios_otro'] = request.POST.get(
                'serviciosOtro', '')

        datos_previos['idiomas'] = request.POST.get('idiomas')
        datos_previos['idiomas_otro'] = ''

        # Verificar si seleccionó "Otro" en idiomas y capturar el texto
        if request.POST.get('idiomas') == '5':
            datos_previos['idiomas_otro'] = request.POST.get('idiomasOtro', '')

        # Actualizar sesión
        request.session['anexo_s4'] = datos_previos

        return redirect('anexo11')

    return render(request, 'Anexo10.html')


def a11(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        # Recuperar datos previos
        datos_previos = request.session.get('anexo_s4', {})

        # Añadir nuevos datos
        datos_previos['publicacion'] = request.POST.get('publicacion')
        datos_previos['publicacion_especifique'] = ''

        # Verificar si seleccionó "Si" en publicacion y capturar el texto
        if request.POST.get('publicacion') == '1':
            datos_previos['publicacion_especifique'] = request.POST.get(
                'publicacionEspecifique', '')

        datos_previos['documentos'] = request.POST.get('documentos')
        datos_previos['documentos_otro'] = ''

        # Verificar si seleccionó "Otro" en documentos y capturar el texto
        if request.POST.get('documentos') == '4':
            datos_previos['documentos_otro'] = request.POST.get(
                'documentosOtro', '')

        datos_previos['calidad'] = request.POST.get('calidad')
        datos_previos['calidad_otra'] = ''

        # Verificar si seleccionó "Otras" en calidad y capturar el texto
        if request.POST.get('calidad') == '3':
            datos_previos['calidad_otra'] = request.POST.get('calidadOtra', '')

        # Actualizar sesión
        request.session['anexo_s4'] = datos_previos

        return redirect('anexo12')

    return render(request, 'Anexo11.html')


def a12(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
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

    return render(request, 'encuestaFinalizada.html')

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
