from django.shortcuts import render, redirect
from core.models import Egresado, Encuesta
from django.shortcuts import render, redirect
from core.models import AnexoS1, AnexoS2, AnexoS3, AnexoS4
from django.contrib import messages


# Create your views here.


def a1(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')

    if request.method == 'POST':
        # Guardar en sesión datos de Anexo1
        request.session['anexo_s1'] = {
            'nombre_completo': request.POST.get('nombre_completo'),
            'redes_sociales': request.POST.get('redes_sociales'),
            'fecha_ingreso': request.POST.get('fecha_ingreso'),
            'telefono': request.POST.get('telefono'),
            'correo': request.POST.get('correo'),
            'fecha_egreso': request.POST.get('fecha_egreso'),
        }
        return redirect('anexo2')
    
    return render(request, 'Anexo1.html')


def a2(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    
    if request.method == 'POST':
        # Recuperar datos guardados desde a1
        datos_previos = request.session.get('anexo_s1', {})

        # Capturar nuevos datos desde el formulario de Anexo2
        datos_previos['titulado'] = request.POST.get('titulado')
        datos_previos['razon_no_titulo'] = request.POST.get('razonNoTitulo')
        datos_previos['razon_no_titulo_otra'] = request.POST.get('razonNoTituloOtra')

        #obtener la conexion con la encuesta correspondiente
        encuesta = Encuesta.objects.filter(curp=curp).order_by('-folioEncuesta').first()

        if encuesta:
            # Crear el registro en la tabla AnexoS1
            AnexoS1.objects.create(
                folioEncuesta=encuesta,
                nombreCompleto=datos_previos.get('nombre_completo'),
                redesSociales=datos_previos.get('redes_sociales'),
                fechaIngreso=datos_previos.get('fecha_ingreso'),
                telefono=datos_previos.get('telefono'),
                correo=datos_previos.get('correo'),
                fechaEgreso=datos_previos.get('fecha_egreso'),
                titulado=datos_previos.get('titulado'),
                razonNoTitulo=datos_previos.get('razon_no_titulo'),
                razonNoTituloOtra=datos_previos.get('razon_no_titulo_otra')
            )

            # Limpiar datos de sesión
            request.session.pop('anexo_s1', None)

            return redirect('anexo3')
        else:
            return redirect('index')  # En caso de que no haya encuesta activa

    return render(request, 'Anexo2.html')



def a3(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo3.html')


def a4(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo4.html')


def a5(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo5.html')


def a6(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo6.html')


def a7(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo7.html')


def a8(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if carrera.lower() not in ['química', 'bioquímica']:
        return redirect('index')  # Carrera no autorizada
    return render(request, 'Anexo8.html')


def a9(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo9.html')


def a10(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo10.html')


def a11(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo11.html')


def a12(request):
    curp = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')

    if not curp or not carrera:
        return redirect('index')  # No hay sesión

    if not any(carrera.lower().replace('í', 'i') in s for s in ['ing. quimica', 'ing. bioquimica']):
        return redirect('index')
    return render(request, 'Anexo12.html')

# TODO agregar acuse y vista agradecimiento
# def a1(request):
#     return render(request, 'Anexo1.html')


# def a1(request):
#     return render(request, 'Anexo1.html')
