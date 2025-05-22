from django.shortcuts import render, redirect
from django.contrib import messages
from SIE import settings
from core.models import Administrador, Egresado, Notificacion
from django.utils import timezone
import datetime
from django.shortcuts import render, redirect
from core.models import EstadoEncuestaCarrera


import random
import string

from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from django.http import JsonResponse
import json

def encuesta_bloqueada(request):
    return render(request, 'encuestaBloqueada.html')

def vista_estado_encuestas(request):
    # Validar sesión de administrador
    rfc_admin = request.session.get('usuario_id')
    if not rfc_admin:
        return redirect('index')

    admin = Administrador.objects.filter(rfc=rfc_admin).first()
    if not admin:
        return redirect('index')

    if request.method == "POST":
        # Solo modificar encuestas si es un admin general o de su propia carrera
        for carrera in EstadoEncuestaCarrera.objects.all():
            if admin.carrera.lower() == "general" or admin.carrera.lower() == carrera.carrera.lower():
                estado = request.POST.get(carrera.carrera)
                carrera.activa = True if estado == 'on' else False
                carrera.save()
        return redirect('vista_estado_encuestas')

    # Solo mostrar carreras que el admin puede modificar
    if admin.carrera.lower() == "general":
        carreras = EstadoEncuestaCarrera.objects.all().order_by('carrera')
    else:
        carreras = EstadoEncuestaCarrera.objects.filter(carrera__iexact=admin.carrera)

    return render(request, 'ActicacionDesactivacion.html', {'carreras': carreras})


# Create your views here.
def index(request):
    tipo = request.session.get('usuario_tipo')
    identificador = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')
    nombre = request.session.get('usuario_nombre')



    # ⏬ Si pasa la verificación, continuar con lo de siempre
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
            admin = Administrador.objects.filter(rfc=tipo).first()
            if admin:
                return render(request, 'modUser.html', {
                    'admin': 'si',
                    'usuario': admin,
                })
            else:
                user = Egresado.objects.filter(curp=tipo).first()
                return render(request, 'modUser.html', {
                    'admin': 'no',
                    'usuario': user,
                })

        except:
            pass
    return render(request, 'modUser.html')


def modCampos(request):
    if request.method == 'POST':
        tipo = request.POST.get('real')
        try:
            admin = Administrador.objects.filter(rfc=tipo).first()
            if admin:
                rfcTemp = request.POST.get('rfc')
                nombreTemp = request.POST.get('nombre')
                correoTemp = request.POST.get('correo')
                carreraTemp = request.POST.get('carrera')

                if rfcTemp != admin.rfc:
                    if Administrador.objects.filter(rfc=rfcTemp).exists():
                        return render(request, "modUser.html", {
                            "error": "Este rfc ya está registrado.",
                            'admin': 'si',
                            'usuario': admin,
                        })
                    else:
                        admin.rfc = rfcTemp
                        admin.save(update_fields=['rfc'])
                        admin = Administrador.objects.filter(
                            rfc=rfcTemp).first()

                if nombreTemp != admin.nombre:
                    admin.nombre = nombreTemp
                    admin.save(update_fields=['nombre'])

                if correoTemp != admin.correo:
                    admin.correo = correoTemp
                    admin.save(update_fields=['correo'])

                if carreraTemp != admin.carrera:
                    admin.carrera = correoTemp
                    admin.save(update_fields=['carrera'])

                return render(request, 'modUser.html', {
                    'admin': 'si',
                    'usuario': admin,
                })

            else:

                user = Egresado.objects.filter(curp=tipo).first()

                curpTemp = request.POST.get('curp')
                nombreTemp = request.POST.get('nombre')
                correoTemp = request.POST.get('correo')
                carreraTemp = request.POST.get('carrera')
                nacioTemp = request.POST.get('fechaNacimiento')
                tituloTemp = True if request.POST.get('titulado') == 'si' else False
                controlTemp = request.POST.get('control')
                sexoTemp = True if request.POST.get('sexo') == 'femenino' else False

                if curpTemp != user.curp:
                    if Egresado.objects.filter(curp=curpTemp).exists():
                        return render(request, "modUser.html", {
                            "error": "Este CURP ya está registrado.",
                            'admin': 'si',
                            'usuario': user,
                        })
                    else:
                        user.curp = curpTemp
                        user.save(update_fields=['curp'])
                        user = Egresado.objects.filter(curp=curpTemp).first()

                if nombreTemp != user.nombre:
                    user.nombre = nombreTemp
                    user.save(update_fields=['nombre'])

                if correoTemp != user.correo:
                    user.correo = correoTemp
                    user.save(update_fields=['correo'])

                if carreraTemp != user.carrera:
                    user.carrera = carreraTemp
                    user.save(update_fields=['carrera'])

                if nacioTemp != user.fechaNacimiento:
                    user.fechaNacimiento = datetime.datetime.strptime(nacioTemp, '%Y-%m-%d').date()
                    user.save(update_fields=['fechaNacimiento'])

                if  tituloTemp != user.titulado:
                    user.titulado = tituloTemp
                    user.save(update_fields=['titulado'])

                if controlTemp != user.noControl:
                    user.noControl = controlTemp
                    user.save(update_fields=['noControl'])

                if  sexoTemp != user.sexo:
                    user.sexo = sexoTemp
                    user.save(update_fields=['sexo'])

                return render(request, 'modUser.html', {
                    'admin': 'no',
                    'usuario': user,
                })

        except ZeroDivisionError as e:
            print(e)
            # pass

    return redirect('modUser')


def newPwd(request):
    if request.method == 'POST': 
        tipo = request.POST.get('personal')
        pwd = generarC()
        try:
            admin = Administrador.objects.filter(rfc=tipo).first()
            admin.contraseña = make_password(pwd)

            send_mail(
                    subject="Esta es tu nueva contraseña",
                    message=f"Hola tu nueva contraseña es:  {pwd} ",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[admin.correo],
                )
            
            admin.save(update_fields=['contraseña'])
        except ZeroDivisionError as e:
            print(e)
    return render(request, 'vistaVerificacionPendiente.html', {
        'admin': 'si'
    })


def generarC():
    
    caracteres = string.ascii_letters + string.digits  # Letras (mayúsculas y minúsculas) + dígitos
    contraseña = ''.join(random.choice(caracteres) for _ in range(9))
    return contraseña

