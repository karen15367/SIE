from django.shortcuts import render

# Create your views here.
def index(request):
    tipo = request.session.get('usuario_tipo')
    clave = request.session.get('usuario_id')
    carrera = request.session.get('usuario_carrera')
    return render(request, 'index.html')