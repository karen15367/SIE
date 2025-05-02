from django.shortcuts import render
import uuid
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from core.models import Egresado

from email.message import EmailMessage
import smtplib

# Create your views here.


def signin(request):
    print('tipo de request', request.method)
    return render(request, "vistaSignUp.html")


def verify(request):
    if request.method == 'POST':
        # todo hacer que al validar el correo se guarde en la base de datos
        try:
            tempUser = Egresado(
                curp=request.POST.get('curp'),
                nombre=request.POST.get('nombre'),
                noControl=request.POST.get('control'),
                correo=request.POST.get('correo'),
                sexo=request.POST.get('sexo'),
                fechaNacimiento=request.POST.get('fechaNacimiento'),
                carrera=request.POST.get('carrera'),
                titulado=request.POST.get('titulado'),
                contraseña=request.POST.get('pwd1'))
            

            
            send_mail(
                subject='Verifica tu cuenta',
                message='Por favor verifica tu cuenta haciendo clic en el siguiente enlace:',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[tempUser.correo],
            )
            
        except:
            print('Error al obtener los datos del email',)
        finally:
            print(tempUser.nombre)


        token = str(uuid.uuid4())
        confirm_url = f"http://127.0.0.1:8000/confirmar/{token}/"
        print('token', token)
        # TODO hacer que se mande el correo


    return render(request, "vistaVerificacion.html", {"mensaje": "Revisa tu correo para confirmar tu cuenta."})


def confirm_email(request, token):
    pass
