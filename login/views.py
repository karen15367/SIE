from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from core.models import Egresado
# Create your views here.


def login(request):
    if request.method == 'POST':
        if request.POST.get('tipo') == '0':
            try:
                if Egresado.objects.get(curp=request.POST.get('curp')) and Egresado.objects.get(contraseña=request.POST.get('password')):
                    #TODO poner la sesion activa y mandar la curp a la vista de index
                    return redirect('/index/')
                
            except Egresado.DoesNotExist:
                messages.info(request, 'modal:Error:El usuario no existe')
                return redirect('/')
        else:
            pass
            # todo hacer la parte admin
    return render(request, "vistaLogin.html")

def signin(request):
    return render(request, "vistaLogin.html")
