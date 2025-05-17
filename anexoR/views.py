from django.shortcuts import render

from core.models import AnexoS1, AnexoS2, AnexoS3, AnexoS4

# Create your views here.


def viewAnexos(request):
    if request.method == 'POST':
        folio = request.POST.get('folio')
        try:
            lista = [
                {'id': 1, 'direccion': 'anexoR/A1'},
                {'id': 2, 'direccion': 'vistaVerificacionPendiente'},
                {'id': 3, 'direccion': ''},
                {'id': 4, 'direccion': 'index'},
            ]
            '''
            lista.append(AnexoS1.objects.get(folioEncuesta_id=folio))
            lista.append(AnexoS2.objects.get(folioEncuesta_id=folio))
            lista.append(AnexoS3.objects.get(folioEncuesta_id=folio))
            lista.append(AnexoS4.objects.get(folioEncuesta_id=folio))
            '''
            return render(request, 'respuestasListado.html', {
                'anexo': True,
                'inicio': False,
                'resultado': True,
                'listado': lista,
            })
        except ZeroDivisionError as e:
            print(e)
            return render(request, 'respuestasListado.html', {
                'anexo': True,
                'inicio': False,
                'listado': False
            })
    else:
        lista = AnexoS1.objects.all()
        resultado = False
        if lista:
            resultado = True

        return render(request, 'respuestasListado.html', {
            'anexo': True,
            'inicio': 'si',
            'resultado': resultado,
            'listado': lista,
        })
    
def viewA1(request):
    return render(request, 'respuestasGrafico.html',{
        'anexo': True,
        'subtitle': 'INFORMACIÓN DEL EGRESADO',
    })
