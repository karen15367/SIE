from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    tipo = request.session.get('usuario_tipo')
    identificador = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')
    
    if not tipo or not identificador:
        # Si no hay sesión activa, redirigir al login
        return redirect('vistaLogin')
    context = {
        'tipo': tipo,
        'identificador': identificador,
        'carrera': carrera,
    }
    return render(request, 'index.html', context)

def cerrar_sesion(request):
    request.session.flush()  # Elimina toda la sesión
    return redirect('/')  # Redirige al login