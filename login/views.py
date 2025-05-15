from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import requests
from SIE import settings
from core.models import Egresado
from core.models import Administrador
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.urls import reverse
from django.core.signing import Signer, BadSignature, SignatureExpired, TimestampSigner

# Create your views here.

def login(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get("g-recaptcha-response")
        data = {
            "secret": settings.RECAPTCHA_PRIVATE_KEY,
            "response": recaptcha_response,
        }
        response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify", data=data)
        result = response.json()

        if not result["success"]:
            # messages.error(request, "¡Completa el reCAPTCHA!")
            return redirect("/")

        identificador = request.POST.get('curp_rfc')
        password = request.POST.get('password')
        if request.POST.get('tipo') == '0':
            try:
                egresado = Egresado.objects.get(curp=identificador)
                if check_password(password, egresado.contraseña):
                    request.session['usuario_tipo'] = 'egresado'
                    request.session['usuario_id'] = egresado.curp
                    request.session['usuario_carrera'] = egresado.carrera
                    request.session['usuario_nombre'] = egresado.nombre
                    # return redirect('index')  # o la que corresponda
                    return redirect('/index/')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Egresado.DoesNotExist:
                messages.error(request, 'El usuario no existe')
            return redirect('/')
        else:
            try:
                admin = Administrador.objects.get(rfc=identificador)
                if check_password(password, admin.contraseña):
                    request.session['usuario_tipo'] = 'admin'
                    request.session['usuario_id'] = admin.rfc
                    request.session['usuario_carrera'] = admin.carrera
                    request.session['usuario_nombre'] = admin.nombre
                    # return redirect('index')  # o admin_home, etc.
                    return redirect('/index/')
                else:
                    messages.error(request, 'Contraseña incorrecta')
            except Administrador.DoesNotExist:
                messages.error(request, 'El usuario no existe')
            return redirect('/')
    return render(request, "vistaLogin.html")


def signin(request):
    return render(request, "vistaLogin.html")


def index(request):
    return render(request, "index.html")


def contrasena(request):
    if request.method == "POST":
        curp = request.POST.get('curp')
        email = request.POST.get('correo')
        try:
            egresado_C = Egresado.objects.get(curp=curp)
            egresado_E = Egresado.objects.get(correo=email)
            
            if egresado_C == egresado_E:
                egresado_C.tempPwd=make_password(request.POST.get("pwd1"))
                egresado_C.save(update_fields=['tempPwd'])
                signer = TimestampSigner()
                signed_token = signer.sign(curp)
                confirm_url = request.build_absolute_uri(
                    reverse("confirm_pwd", args=[signed_token]))
                send_mail(
                    subject="Confirma tu nueva contraseña de SIE",
                    message=f"Hola {egresado_C.nombre}, confirma tu contraseña: {confirm_url}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                )

            else:
                print('no existe')
        except Egresado.DoesNotExist:
            print('pichyle')

    return render(request, "vistaContrasena.html")

def confirm_pwd(request, token):
        signer = TimestampSigner()
        try:
            curp = signer.unsign(token, max_age=1800)
            egresado = Egresado.objects.get(curp=curp)

            print(f'contraseña temporal {egresado.tempPwd}')

            egresado.contraseña = egresado.tempPwd
            egresado.tempPwd=None
            egresado.save(update_fields=['contraseña'])
            egresado.save(update_fields=['tempPwd'])
            return render(request, "vistaVerificacion.html")
        except SignatureExpired:
            return HttpResponse("El enlace ha expirado.", status=400)
        except BadSignature:
            return HttpResponse("Enlace inválido.", status=400)
    
