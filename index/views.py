from django.shortcuts import redirect, render

# Create your views here.
def index(request):
    tipo = request.session.get('usuario_tipo')
    clave = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')
    return render(request, 'index.html')

def cerrar_sesion(request):
    request.session.flush()  # Elimina toda la sesión
    return redirect('/')  # Redirige al login