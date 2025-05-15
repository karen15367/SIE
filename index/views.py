from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Administrador, Egresado, Notificacion
from django.utils import timezone
import datetime
from django.http import JsonResponse
import json


# Create your views here.
def index(request):
    tipo = request.session.get('usuario_tipo')
    identificador = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')
    nombre = request.session.get('usuario_nombre')

    if not tipo or not identificador:
        # Si no hay sesión activa, redirigir al login
        return redirect('vistaLogin')

    fecha_actual = timezone.now().date()
    avisos_activos = Notificacion.objects.filter(
        fechaInicio__lte=fecha_actual,
        fechaFin__gte=fecha_actual
    ).order_by('-fechaInicio')

    context = {
        'tipo': tipo,
        'identificador': identificador,
        'carrera': carrera,
        'nombre': nombre,
        'avisos': avisos_activos,
    }
    return render(request, 'index.html', context)


def cerrar_sesion(request):
    request.session.flush()  # Elimina toda la sesión
    return redirect('/')  # Redirige al login


def vistaSignUpAdmin(request):
    return render(request, 'vistaSignUpAdmin.html')


def crear_aviso(request):
    # Verificar si el usuario es administrador
    try:
        tipo = request.session.get('usuario_tipo')
        if tipo != 'admin':
            messages.error(request, 'No tienes permisos para crear avisos')
            return redirect('index')

        if request.method == 'POST':
            # Obtener datos del formulario
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_fin_str = request.POST.get('fecha_fin')

            # Validar que todos los campos estén presentes
            if not titulo or not descripcion or not fecha_inicio_str or not fecha_fin_str:
                messages.error(request, 'Todos los campos son obligatorios')
                return render(request, 'crear_aviso.html')

            try:
                # Convertir strings de fecha a objetos datetime
                fecha_inicio = datetime.datetime.strptime(
                    fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.datetime.strptime(
                    fecha_fin_str, '%Y-%m-%d').date()

                # Validar que la fecha de inicio no sea posterior a la fecha de fin
                if fecha_inicio > fecha_fin:
                    messages.error(
                        request, 'La fecha de inicio no puede ser posterior a la fecha de fin')
                    return render(request, 'crear_aviso.html')

                # Crear el aviso
                aviso = Notificacion(
                    titulo=titulo,
                    descripcion=descripcion,
                    fechaInicio=fecha_inicio,
                    fechaFin=fecha_fin
                )
                aviso.save()

                messages.success(request, 'Aviso creado correctamente')
                return redirect('index')

            except ValueError:
                messages.error(
                    request, 'Formato de fecha incorrecto. Utiliza el formato YYYY-MM-DD')
                return render(request, 'crear_aviso.html')
        else:
            # Si la petición es GET, mostrar el formulario
            return render(request, 'crear_aviso.html')
    except:
        pass


def editar_aviso(request, idNotificacion):
    try:
        # Verificar si el usuario es administrador
        tipo = request.session.get('usuario_tipo')
        identificador = request.session.get('usuario_id')
        carrera = request.session.get('usuario_carrera')
        nombre = request.session.get('usuario_nombre')

        if tipo != 'admin':
            messages.error(request, 'No tienes permisos para editar avisos')
            return redirect('index')

        try:
            aviso = Notificacion.objects.get(idNotificacion=idNotificacion)
        except Notificacion.DoesNotExist:
            messages.error(request, 'El aviso no existe')
            return redirect('index')

        # Obtener avisos activos para el popup
        fecha_actual = timezone.now().date()
        avisos_activos = Notificacion.objects.filter(
            fechaInicio__lte=fecha_actual,
            fechaFin__gte=fecha_actual
        ).order_by('-fechaInicio')

        if request.method == 'POST':
            # Obtener datos del formulario
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_fin_str = request.POST.get('fecha_fin')

            # Validar que todos los campos estén presentes
            if not titulo or not descripcion or not fecha_inicio_str or not fecha_fin_str:
                messages.error(request, 'Todos los campos son obligatorios')
                return render(request, 'editar_aviso.html', {
                    'aviso': aviso,
                    'tipo': tipo,
                    'identificador': identificador,
                    'carrera': carrera,
                    'nombre': nombre,
                    'avisos': avisos_activos
                })

            try:
                # Convertir strings de fecha a objetos datetime
                fecha_inicio = datetime.datetime.strptime(
                    fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.datetime.strptime(
                    fecha_fin_str, '%Y-%m-%d').date()

                # Validar que la fecha de inicio no sea posterior a la fecha de fin
                if fecha_inicio > fecha_fin:
                    messages.error(
                        request, 'La fecha de inicio no puede ser posterior a la fecha de fin')
                    return render(request, 'editar_aviso.html', {
                        'aviso': aviso,
                        'tipo': tipo,
                        'identificador': identificador,
                        'carrera': carrera,
                        'nombre': nombre,
                        'avisos': avisos_activos
                    })

                # Actualizar el aviso
                aviso.titulo = titulo
                aviso.descripcion = descripcion
                aviso.fechaInicio = fecha_inicio
                aviso.fechaFin = fecha_fin
                aviso.save()

                messages.success(request, 'Aviso actualizado correctamente')
                return redirect('index')

            except ValueError:
                messages.error(
                    request, 'Formato de fecha incorrecto. Utiliza el formato YYYY-MM-DD')
                return render(request, 'editar_aviso.html', {
                    'aviso': aviso,
                    'tipo': tipo,
                    'identificador': identificador,
                    'carrera': carrera,
                    'nombre': nombre,
                    'avisos': avisos_activos
                })
        else:
            # Si la petición es GET, mostrar el formulario con los datos del aviso
            return render(request, 'editar_aviso.html', {
                'aviso': aviso,
                'tipo': tipo,
                'identificador': identificador,
                'carrera': carrera,
                'nombre': nombre,
                'avisos': avisos_activos
            })
    except:
        pass


def resultados(request):
    if request.method == 'POST':
        carrera = request.POST.get('carrera')
        tipo = request.POST.get('tipo')
        admin = request.POST.get('switch')
        try:
            if carrera == 'Todos':
                if admin:
                    usuarios = Administrador.objects.all()
                    return render(request, 'vistaResultados.html', {
                        'usuarios': usuarios,
                        'admin': 'si'
                    })
                else:
                    usuarios = Egresado.objects.all()
                    return render(request, 'vistaResultados.html', {
                        'usuarios': usuarios,
                        'admin': 'no'
                    })
            elif carrera:
                if admin:
                    usuarios = Administrador.objects.filter(carrera=carrera)
                    return render(request, 'vistaResultados.html', {
                        'usuarios': usuarios,
                        'admin': 'si'
                    })
                else:
                    usuarios = Egresado.objects.filter(carrera=carrera)
                    return render(request, 'vistaResultados.html', {
                        'usuarios': usuarios,
                        'admin': 'no'
                    })
            else:
                if admin:
                    usuarios = Administrador.objects.filter(rfc=tipo)
                    return render(request, 'vistaResultados.html', {
                        'usuarios': usuarios,
                        'admin': 'si'
                    })
                else:
                    usuarios = Egresado.objects.filter(curp=tipo)
                    return render(request, 'vistaResultados.html', {
                        'usuarios': usuarios,
                        'admin': 'no'
                    })
        except:
            pass
    return render(request, 'vistaResultados.html')


def modUser(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')

        try:
            admin = Administrador.objects.filter(rfc=tipo)
            user = Egresado.objects.filter(curp=tipo)
            if user:
                print('pichule')
            elif admin:
                print('pichuleichon')
        except:
            pass

    return render(request, 'modUser.html')
