import os
from django.shortcuts import render, redirect
from datetime import date
from django.contrib import messages
from datetime import datetime
from django.http import HttpResponse
from . import acuse
from core.models import (
    Encuesta, EncuestaS1, EncuestaS2, EncuestaS3, EncuestaS3Empresa,
    EncuestaS4, EncuestaS5, Egresado
)

def calcular_lapso():
    hoy = date.today()
    año = hoy.year
    semestre = 1 if hoy.month <= 6 else 2
    return f"{año}-{semestre}"

def index(request):
    return render(request, 'index.html')


def e1(request):
    curp = request.session.get('usuario_id')
    if not curp:
        return redirect('index')

    if request.method == 'POST':
        egresado = Egresado.objects.filter(curp=curp).first()
        encuesta = Encuesta.objects.create(
            curp=egresado,
            fechaInicio=date.today(),
            lapso=calcular_lapso()
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
    return render(request, 'encuesta1.html')

def e2(request):
    if request.method == 'POST':
        datos = request.session.get('encuesta_s1', {})
        print("Datos recibidos:", request.POST)
        datos.update({
            'carrera': request.POST.get('carrera'),
            'especialidad': request.POST.get('Especialidad'),
            'fechaIngreso': request.POST.get('fechaingreso'),
            'fechaEgreso': request.POST.get('fechaEgreso'),
            'titulado': request.POST.get('titulo'),
            'dominioIngles': request.POST.get('dominio'),
            'otroIdioma': request.POST.get('idioma'),
            'manejoPaquetes': request.POST.get('paquetes'),
            'especificarPaquetes': request.POST.get('paquetesE')
        })
        print("Datos recibidos:", request.POST)
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        EncuestaS1.objects.create(folioEncuesta=encuesta, **datos)
        request.session.pop('encuesta_s1', None)
        return redirect('e3')
    return render(request, 'encuesta2.html')

def e3(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        print("Datos recibidos:", request.POST)
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        EncuestaS2.objects.create(
            folioEncuesta=encuesta,
            calidadDocentes=request.POST.get('calidadDocentes'),
            planEstudios=request.POST.get('planEstudios'),
            oportunidadesProyectos=request.POST.get('oportunidadesProyectos'),
            enfasisInvestigacion=request.POST.get('enfasisInvestigacion'),
            satisfaccionCondiciones=request.POST.get('satisfaccionCondiciones'),
            experienciaResidencia=request.POST.get('experienciaResidencia')
        )
        return redirect('e4')
    return render(request, 'encuesta3.html')

def e4(request):
    if request.method == 'POST':
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
        EncuestaS3.objects.create(folioEncuesta=encuesta, **datos)
        if actividad in [2, 4]:
            return redirect('e9')
        return redirect('e5')
    return render(request, 'encuesta4.html')

def e5(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        hablarPorcentaje = request.POST.get('hablarPorcentaje')
        hablarPorcentaje = int(hablarPorcentaje) if hablarPorcentaje else 0
        escribirPorcentaje = request.POST.get('escribirPorcentaje')
        escribirPorcentaje = int(escribirPorcentaje) if escribirPorcentaje else 0
        leerPorcentaje = request.POST.get('leerPorcentaje')
        leerPorcentaje = int(leerPorcentaje) if leerPorcentaje else 0
        escucharPorcentaje = request.POST.get('escucharPorcentaje')
        escucharPorcentaje = int(escucharPorcentaje) if escucharPorcentaje else 0
        EncuestaS3.objects.filter(folioEncuesta=encuesta).update(
            medioEmpleo=request.POST.get('medioEmpleo'),
            medioEmpleoOtro=request.POST.get('medioEmpleoOtro'),
            requisitosContratacion=request.POST.get('requisitosContratacion'),
            requisitosContratacionOtro=request.POST.get('requisitosContratacionOtro'),
            idiomaUtiliza=request.POST.get('idiomaUtiliza'),
            idiomaUtilizaOtro=request.POST.get('idiomaUtilizaOtro'),
            hablarPorcentaje=hablarPorcentaje,
            escribirPorcentaje=escribirPorcentaje,
            leerPorcentaje=leerPorcentaje,
            escucharPorcentaje=escucharPorcentaje
        )
        return redirect('e6')
    return render(request, 'encuesta5.html')

def e6(request):
    if request.method == 'POST':
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
    return render(request, 'encuesta6.html')

def e7(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
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
        EncuestaS3Empresa.objects.create(folioEncuesta=encuesta, **datos)
        request.session.pop('empresa', None)
        return redirect('e9')
    return render(request, 'encuesta8.html')

def e9(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        EncuestaS4.objects.create(
            folioEncuesta=encuesta,
            eficiencia=request.POST.get('eficiencia'),
            formacion=request.POST.get('formacion'),
            utilidad=request.POST.get('utilidad')
        )
        return redirect('e10')
    return render(request, 'encuesta9.html')

def e10(request):
    if request.method == 'POST':
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
    return render(request, 'encuesta11.html')

def e12(request):
    if request.method == 'POST':
        folio = request.session['folio_encuesta']
        encuesta = Encuesta.objects.get(folioEncuesta=folio)
        datos = request.session.get('s5', {})
        datos['comentariosSugerencias'] = request.POST.get('comentariosSugerencias')
        EncuestaS5.objects.create(folioEncuesta=encuesta, **datos)
        encuesta.fechaFin = date.today()
        encuesta.save()
        request.session.pop('s5', None)
        return redirect('encuesta_finalizada')
    return render(request, 'encuesta12.html')

def encuesta_finalizada(request):
    curp = request.session.get('usuario_id')
    if not curp:
        return redirect('index')

    egresado = Egresado.objects.filter(curp=curp).first()
    encuesta = Encuesta.objects.filter(curp=egresado).order_by('-folioEncuesta').first()

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
