from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from core.models import Egresado
from django.contrib.auth.hashers import check_password
# Create your views here.


def login(request):
    if request.method == 'POST':
        if request.POST.get('tipo') == '0':
            try:
                egresado = Egresado.objects.get(curp=request.POST.get('curp'))
                if check_password(request.POST.get('password'), egresado.contraseña):
                    # TODO: poner la sesión activa y mandar la curp a la vista de index
                    return redirect('/index/')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Egresado.DoesNotExist:
                messages.error(request, 'El usuario no existe')
            return redirect('/')
        else:
            pass
            # todo hacer la parte admin
    return render(request, "vistaLogin.html")

def signin(request):
    return render(request, "vistaLogin.html")
