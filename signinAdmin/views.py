from decouple import config
from django.shortcuts import render
from django.conf import settings
from core.models import Administrador
from core.models import AdministradorTemporal
from datetime import datetime
from django.contrib.auth.hashers import make_password
import uuid
from django.core.signing import Signer, BadSignature, SignatureExpired, TimestampSigner
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.db.utils import IntegrityError
from django.utils.timezone import now
from datetime import timedelta



# * Create your views here. comentar esto al migrar la base de datos
#AdministradorTemporal.objects.filter(fecha_creacion__lt=now() - timedelta(hours=1)).delete()

def vistaSignUpAdmin(request):
    return render(request, "vistaSignUpAdmin.html")


def vistaVerificacionPendiente(request):
    return render(request, "vistaVerificacionPendiente.html")


def vistaLogin(request):
    return render(request, 'vistaLogin.html')


def verify(request):
    try:
        if request.method == "POST":
            rfc = request.POST.get("rfc")
            if len(rfc) > 13:
                return HttpResponse("El RFC no puede tener más de 13 caracteres.", status=400)
            
            if Administrador.objects.filter(rfc=rfc).exists():
                return render(request, "vistaSignUpAdmin.html", {
                    "error": "Este RFC ya ha sido registrado."
                })
                
            temp = AdministradorTemporal(
                rfc=rfc,
                nombre=request.POST.get("nombre"),
                correo=request.POST.get("correo"),
                carrera=request.POST.get("carrera"),
                contraseña=make_password(request.POST.get("pwd1")),
            )
            temp.save()

            # Firmar el token
            signer = TimestampSigner()
            signed_token = signer.sign(rfc)
            confirm_url = request.build_absolute_uri(reverse("signinAdmin:confirm_email", args=[signed_token]))
            
            send_mail(
                subject="Verifica tu cuenta en SIE",
                message=f"Hola {temp.nombre}, confirma tu cuenta: {confirm_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[temp.correo],
            )
            # print("Host:", settings.EMAIL_HOST)
            # print("User:", settings.EMAIL_HOST_USER)
            return render(request, "vistaVerificacionPendiente.html")
        return render(request, "vistaSignUpAdmin.html")
    except:
        pass


def confirm_email(request, token):
    try:
        print('llega')
        signer = TimestampSigner()
        try:
            # válido por 1 día = 86400 segundos
            rfc = signer.unsign(token, max_age=1800)
            temp = AdministradorTemporal.objects.get(rfc=rfc)

            print('entra')
            try:
                Administrador.objects.create(
                    rfc=temp.rfc,
                    nombre=temp.nombre,
                    correo=temp.correo,
                    carrera=temp.carrera,
                    contraseña=temp.contraseña,
                )
                temp.delete()
                return render(request, "vistaVerificacion.html")
            except IntegrityError:
                return HttpResponse("Este administrador ya fue registrado.", status=400)
            
        except AdministradorTemporal.DoesNotExist:
            return HttpResponse("El registro temporal no existe o ya fue confirmado.", status=400)
        except SignatureExpired:
            return HttpResponse("El enlace ha expirado.", status=400)
        except BadSignature:
            return HttpResponse("Enlace inválido.", status=400)
    except:
        pass