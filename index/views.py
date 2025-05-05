from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Notificacion
from django.utils import timezone
import datetime


# Create your views here.
def index(request):
    tipo = request.session.get('usuario_tipo')
    identificador = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')
    nombre = request.session.get('usuario_nombre')
    
    if not tipo or not identificador:
        # Si no hay sesión activa, redirigir al login
        return redirect('vistaLogin')
    context = {
        'tipo': tipo,
        'identificador': identificador,
        'carrera': carrera,
        'nombre': nombre,
    }
    return render(request, 'index.html', context)

def cerrar_sesion(request):
    request.session.flush()  # Elimina toda la sesión
    return redirect('/')  # Redirige al login

def crear_aviso(request):
    # Verificar si el usuario es administrador
    tipo = request.session.get('usuario_tipo')
    if tipo != 'admin':
        messages.error(request, 'No tienes permisos para crear avisos')
        return redirect('/index/')
    
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
            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            
            # Validar que la fecha de inicio no sea posterior a la fecha de fin
            if fecha_inicio > fecha_fin:
                messages.error(request, 'La fecha de inicio no puede ser posterior a la fecha de fin')
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
            return redirect('/index/')
            
        except ValueError:
            messages.error(request, 'Formato de fecha incorrecto. Utiliza el formato YYYY-MM-DD')
            return render(request, 'crear_aviso.html')
    else:
        # Si la petición es GET, mostrar el formulario
        return render(request, 'crear_aviso.html')
