from decouple import config
from django.shortcuts import render
from django.conf import settings
from core.models import Egresado
from datetime import datetime
from django.contrib.auth.hashers import make_password
import uuid
from django.core.signing import Signer, BadSignature, SignatureExpired, TimestampSigner
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.conf import settings
from datetime import datetime
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError


# * Create your views here.


def signin(request):
    return render(request, "vistaSignUp.html")


def vistaVerificacionPendiente(request):
    return render(request, "vistaVerificacionPendiente.html")


def vistaLogin(request):
    return render(request, 'vistaLogin.html')


def verify(request):
    if request.method == "POST":
        fechaN = request.POST.get("fechaNacimiento")
        sexo = request.POST.get("sexo") != "masculino"
        titulo = request.POST.get("titulado") != "no"

        tempUser = {
            "curp": request.POST.get("curp"),
            "nombre": request.POST.get("nombre"),
            "control": request.POST.get("control"),
            "correo": request.POST.get("correo"),
            "sexo": sexo,
            "fechaNacimiento": fechaN,
            "carrera": request.POST.get("carrera"),
            "titulado": titulo,
            "fechaEgreso": fechaN,
            "pwd1": request.POST.get("pwd1")
        }

        # Guardar temporalmente
        request.session["registro_egresado"] = tempUser

        # Firmar el token
        signer = TimestampSigner()
        signed_token = signer.sign(request.POST.get("curp"))
        confirm_url = request.build_absolute_uri(
            reverse("confirm_email", args=[signed_token]))
        print(request.POST.get("correo"))
        send_mail(
            subject="Verifica tu cuenta en SIE",
            message=f"Hola {tempUser['nombre']}, confirma tu cuenta: {confirm_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[tempUser["correo"]],
        )
        # print("Host:", settings.EMAIL_HOST)
        # print("User:", settings.EMAIL_HOST_USER)
        return render(request, "vistaVerificacionPendiente.html")
    return render(request, "vistaSignUp.html")


def confirm_email(request, token):
    print('llega')
    signer = TimestampSigner()
    try:
        # válido por 1 día = 86400 segundos
        curp = signer.unsign(token, max_age=1800)
        tempUser = request.session.get("registro_egresado")

        if not tempUser or tempUser.get("curp") != curp:
            return HttpResponse("Tu sesión ha expirado o los datos no coinciden.", status=400)

        if "pwd1" not in tempUser:
            return HttpResponse("Faltan datos en sesión (pwd1)", status=400)

        # Validar campos obligatorios
        required_fields = ['nombre', 'control', 'correo', 'sexo','fechaNacimiento', 'carrera', 'titulado', 'fechaEgreso', 'pwd1']
        for field in required_fields:
            if field not in tempUser:
                return HttpResponse(f"Falta el campo: {field}", status=400)
        print('entra')
        try:
            print('registra')
            Egresado.objects.create(
                curp=curp,
                nombre=tempUser['nombre'],
                noControl=tempUser['control'],
                correo=tempUser['correo'],
                sexo=tempUser['sexo'],
                fechaNacimiento=parse_date(tempUser['fechaNacimiento']),
                carrera=tempUser['carrera'],
                titulado=tempUser['titulado'],
                fechaEgreso=parse_date(tempUser['fechaEgreso']),
                contraseña=make_password(tempUser['pwd1']),
            )
            del request.session["registro_egresado"]
            return render(request, "vistaVerificacion.html")

        except IntegrityError:
            return HttpResponse("Este egresado ya fue registrado.", status=400)

    except SignatureExpired:
        return HttpResponse("El enlace ha expirado.", status=400)
    except BadSignature:
        return HttpResponse("Enlace inválido.", status=400)
