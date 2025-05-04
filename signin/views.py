from decouple import config
from django.shortcuts import render
from django.conf import settings
from core.models import Egresado
import uuid
import resend
from django.core.signing import Signer, BadSignature, SignatureExpired, TimestampSigner
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.conf import settings

# * Create your views here.


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
            # TODO hacer que se mande el correo de verificación
            signer = TimestampSigner()
            signer = TimestampSigner()
            signed_token = signer.sign(tempUser.curp)  # o tempUser.correo si prefieres
            confirm_url = f"http://127.0.0.1:8000/confirmar/{signed_token}/"
            print('token', token)

            # TODO PASARSE A RESEND
            resend.api_key = config("RESEND_API_KEY")
            print(f'{resend.api_key} resend api key')
            params = {
                "from": "onboarding@resend.dev",
                "to": [tempUser.correo],
                "subject": "Verifica tu cuenta en SIE",
                "html": f"""
                    <h1>¡Hola, {tempUser.nombre}!</h1>
                    <p>Gracias por registrarte en SIE. Por favor verifica tu cuenta haciendo clic en el siguiente enlace:</p>
                    <a href="{confirm_url}">Confirmar cuenta</a>
                    <p>Si no fuiste tú, puedes ignorar este correo.</p>
                """
            }
            resend.Emails.send(params)

        except ZeroDivisionError as e:
            print(f'Error al obtener los datos del email {e}')
        finally:
            print(tempUser.correo)
    return render(request, "vistaVerificacion.html", {"mensaje": "Revisa tu correo para confirmar tu cuenta."})


def confirm_email(request, token):
    pass

    # // se manda el correo ¡?
    '''
        #! NO
        send_mail(
            subject='Verifica tu cuenta',
            message='Por favor verifica tu cuenta haciendo clic en el siguiente enlace:',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[tempUser.correo],
        )
        '''
