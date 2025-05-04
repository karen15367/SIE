from decouple import config
from django.shortcuts import render
from django.conf import settings
from core.models import Egresado
from datetime import datetime
from django.contrib.auth.hashers import make_password
import uuid
import resend
from django.core.signing import Signer, BadSignature, SignatureExpired, TimestampSigner
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from django.conf import settings

# * Create your views here.


def signin(request):
    return render(request, "vistaSignUp.html")


def verify(request):
    if request.method == 'POST':
        # todo hacer que al validar el correo se guarde en la base de datos
        # * para la fecha de nacimiento y egreso
        fechaN = request.POST.get('fechaNacimiento')
        # * para el sexo
        if request.POST.get('sexo') is 'Masculino':
            sexo = False
        else:
            sexo = True
        # * para el titulo
        if request.POST.get('titulado') is 'no':
            titulo = False
        else:
            titulo = True

        try:
            '''
            #TODO hacer que al validar correo se guarde en la base de datos
            Egresado.objects.create(
                curp=request.POST.get('curp'),
                nombre=request.POST.get('nombre'),
                noControl=request.POST.get('control'),
                correo=request.POST.get('correo'),
                sexo=sexo,
                fechaNacimiento=datetime.strptime(fechaN, '%Y-%m-%d').date(),
                carrera=request.POST.get('carrera'),
                titulado=titulo,
                fechaEgreso=datetime.strptime(fechaN, '%Y-%m-%d').date(),
                contraseña=make_password( request.POST.get('pwd1')))
            '''
            # TODO hacer que se mande el correo de verificación
            signer = TimestampSigner()
            signer = TimestampSigner()
            signed_token = signer.sign(tempUser.curp)  # o tempUser.correo si prefieres
            confirm_url = f"http://127.0.0.1:8000/confirmar/{signed_token}/"
            print('token', token)

            # TODO PASARSE A RESEND
            resend.api_key = config("RESEND_API_KEY")
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
                "to": [request.POST.get('correo')],
                "subject": "Hello world",
                "html": "pvto resend tambien me dio problemas"
            }
            #!resend.Emails.send(params)

        except ZeroDivisionError as e:
            print(f'{e}')
        finally:
            print(request.POST.get('correo'))
    return render(request, "vistaVerificacion.html")


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
