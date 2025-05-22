#signin/views.py
from decouple import config
from django.shortcuts import render
from django.conf import settings
from core.models import Egresado
from core.models import EgresadoTemporal
from datetime import datetime
from django.contrib.auth.hashers import make_password
import uuid
from django.core.signing import Signer, BadSignature, SignatureExpired, TimestampSigner
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta


# * Create your views here. comentar esto al migrar la base de datos
# EgresadoTemporal.objects.filter(fecha_creacion__lt=now() - timedelta(hours=1)).delete()

def signin(request):
    print(">>> Estoy en signin")
    return render(request, "vistaSignUp.html")



def vistaVerificacionPendiente(request):
    return render(request, "vistaVerificacionPendiente.html")


def vistaLogin(request):
    return render(request, 'vistaLogin.html')


def verify(request):
    print(">>> Entrando a verify")
    if request.method == "POST":
        try:
            print(">>> Método POST detectado")

            curp = request.POST.get("curp", "").strip().lower()

            egresado_existente = Egresado.objects.filter(curp=curp).first()
            if egresado_existente:
                if egresado_existente.correo and egresado_existente.nombre != "Pendiente":
                    return render(request, "vistaSignUp.html", {
                        "error": "Este CURP ya está registrado por un egresado real."
                    })
                else:
                    print(">>> CURP corresponde a un egresado fantasma; se actualizará.")

            print(">>> CURP validado correctamente")

            fechaN = request.POST.get("fechaNacimiento")
            sexo = request.POST.get("sexo") != "masculino"
            titulado = request.POST.get("titulado") != "no"

            temp = EgresadoTemporal(
                curp=curp,
                nombre=request.POST.get("nombre"),
                no_control=request.POST.get("control"),
                correo=request.POST.get("correo"),
                sexo=sexo,
                fecha_nacimiento=fechaN,
                carrera=request.POST.get("carrera"),
                titulado=titulado,
                fecha_egreso=fechaN,
                contraseña=make_password(request.POST.get("pwd1"))
            )
            temp.save()

            signer = TimestampSigner()
            signed_token = signer.sign(curp)
            confirm_url = request.build_absolute_uri(
                reverse("confirm_email", args=[signed_token])
            )

            print(">>> Enviando correo a:", temp.correo)
            send_mail(
                subject="Verifica tu cuenta en SIE",
                message=f"Hola {temp.nombre}, confirma tu cuenta: {confirm_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[temp.correo],
            )
            print(">>> Correo enviado correctamente")

            return render(request, "vistaVerificacionPendiente.html")

        except Exception as e:
            print(">>> ERROR durante verificación:", str(e))

    print(">>> Renderizando vistaSignUp.html final")
    return render(request, "vistaSignUp.html")


def confirm_email(request, token):
    try:
        signer = TimestampSigner()

        try:
            # Token válido por 30 minutos
            curp = signer.unsign(token, max_age=1800)
            curp = curp.strip().lower()  # Normalizar la CURP

            # Buscar egresado temporal
            temp = EgresadoTemporal.objects.get(curp=curp)

            # Validar que todos los datos existen (por seguridad extra)
            campos_requeridos = [
                temp.nombre, temp.no_control, temp.correo,
                temp.fecha_nacimiento, temp.carrera,
                temp.fecha_egreso, temp.contraseña
            ]
            if any(valor is None for valor in campos_requeridos):
                return HttpResponse("Faltan datos en el registro temporal.", status=400)

            # Crear o actualizar el egresado
            Egresado.objects.update_or_create(
                curp=curp,
                defaults={
                    'nombre': temp.nombre,
                    'noControl': temp.no_control,
                    'correo': temp.correo,
                    'sexo': temp.sexo,
                    'fechaNacimiento': temp.fecha_nacimiento,
                    'carrera': temp.carrera,
                    'titulado': temp.titulado,
                    'fechaEgreso': temp.fecha_egreso,
                    'contraseña': temp.contraseña  # Ya está hasheada
                }
            )

            # Eliminar el temporal
            temp.delete()

            return render(request, "vistaVerificacion.html")

        except EgresadoTemporal.DoesNotExist:
            return HttpResponse("El registro temporal no existe o ya fue confirmado.", status=400)
        except SignatureExpired:
            return HttpResponse("El enlace ha expirado.", status=400)
        except BadSignature:
            return HttpResponse("Enlace inválido.", status=400)

    except Exception as e:
        print(">>> ERROR en confirm_email:", str(e))
        return HttpResponse("Error inesperado al confirmar el correo.", status=500)
