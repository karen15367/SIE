from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from core.models import Egresado
from core.models import Administrador
from django.contrib.auth.hashers import check_password
# Create your views here.


def login(request):
    if request.method == 'POST':
        if request.POST.get('tipo') == '0':
            try:
                egresado = Egresado.objects.get(curp=curp)
                if check_password(password, egresado.contraseña):
                    request.session['usuario_tipo'] = 'egresado'
                    request.session['usuario_id'] = egresado.curp
                    request.session['usuario_carrera'] = egresado.carrera
                    return redirect('vistaIndex')  # o la que corresponda
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Egresado.DoesNotExist:
                messages.error(request, 'El usuario no existe')
            return redirect('/')
        else:
            try:
                admin = Administrador.objects.get(rfc=curp)
                if check_password(password, admin.contraseña):
                    request.session['usuario_tipo'] = 'admin'
                    request.session['usuario_id'] = admin.rfc
                    request.session['usuario_carrera'] = admin.carrera
                    return redirect('vistaIndex')  # o admin_home, etc.
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Administrador.DoesNotExist:
                messages.error(request, 'El usuario no existe')
            return redirect('/')
    return render(request, "vistaLogin.html")

def signin(request):
    return render(request, "vistaLogin.html")
