from django.shortcuts import render

from core.models import EncuestaS1

# Create your views here.


def viewEncuesta(request):
    if request.method == 'POST':

        try:
            lista = [
                {'id': 'PERFIL DEL EGRESADO', 'direccion': 'encuestaR/E1'},
                {'id': 'SITUACIÓN LABORAL', 'direccion': 'anexoR/A2'},
                {'id': 'PLAN DE ESTUDIOS / INSTITUCIÓN ', 'direccion': 'anexoR/A3'},
                {'id': 'DESEMPEÑO LABORAL', 'direccion': 'anexoR/A4'},
            ]
        except:
            pass

        
        return render(request, 'respuestasListado.html', {
            'anexo': False,
            'inicio': False,
            'resultado': True,
            'listado': lista,
        })
    else:
        lista = EncuestaS1.objects.all()
        resultado = False
        if lista:
            resultado = True

        return render(request, 'respuestasListado.html', {
            'anexo': False,
            'inicio': 'si',
            'resultado': resultado,
            'listado': lista,
        })


def viewE1(request):
    answer = EncuestaS1.objects.all()

    sF =  EncuestaS1.objects.filter(sexo=1).count()
    sM =  EncuestaS1.objects.filter(sexo=0).count()
    
    e1 =  EncuestaS1.objects.filter(estadoCivil=1).count()
    e2 =  EncuestaS1.objects.filter(estadoCivil=2).count()
    
    t1 =  EncuestaS1.objects.filter(titulado=0).count()
    t2 =  EncuestaS1.objects.filter(titulado=1).count()
    
    p1 =  EncuestaS1.objects.filter(titulado=0).count()
    p2 =  EncuestaS1.objects.filter(titulado=1).count()


    return render(request, 'layouts/E1.html', {
        'anexo': True,
        'subtitle': 'PERFIL DEL EGRESADO',
        'sexo': {'si': sF, 'no':sM},
        'estado': {'si': e1, 'no':e2},
        'titulado': {'si': t1, 'no':t2},
        'paquetes': {'si': p1, 'no':p2},
    })

