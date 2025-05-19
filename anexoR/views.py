from django.shortcuts import render

from django.db.models import Count, Q
from core.models import AnexoS1, AnexoS2, AnexoS3, AnexoS4

# Create your views here.


def viewAnexos(request):
    if request.method == 'POST':
        folio = request.POST.get('folio')
        try:
            lista = [
                {'id': 'DATOS GENERALES', 'direccion': 'anexoR/A1'},
                {'id': 'SITUACIÓN LABORAL', 'direccion': 'anexoR/A2'},
                {'id': 3, 'direccion': ''},
                {'id': 4, 'direccion': 'index'},
            ]

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
    answer = AnexoS1.objects.all()
    titulo = 0
    sinTitulo = 0

    for a in answer:
        if a.titulado == 1:
            titulo += 1
        else:
            sinTitulo += 1

    return render(request, 'layouts/A1.html', {
        'anexo': True,
        'subtitle': 'INFORMACIÓN DEL EGRESADO',
        'titulo': {'si': titulo, 'no': sinTitulo},
    })


def viewA2(request):
    answer = AnexoS2.objects.all()

    trabaja = noTrabaja = relacion = noRelacion = 0

    a1 = a2 = a3 = a4 = 0

    t1 = t2 = t3 = 0

    s1 = s2 = s3 = s4 = 0

    p1 = p2 = p3 = p4 = p5 = p6 = p7 = 0

    d1 = d2 = d3 = d4 = d5 = d6 = d7 = 0

    m1 = m2 = m3 = m4 = m5 = 0

    g1 = g2 = g3 = g4 = 0

    for a in answer:
        if a.trabaja == 1:
            # * El egresado trabaja
            trabaja += 1
            # * Relación entre su trabajo y su carrera
            if a.relacionTrabajoCarrera == 1:
                relacion += 1
                # * tiempo en coseguir empleo relacionado con la carrera
                if a.tiempoTrabajoRelacionado == 1:
                    t1 += 1
                elif a.tiempoTrabajoRelacionado == 2:
                    t2 += 1
                elif a.tiempoTrabajoRelacionado == 3:
                    t3 += 1
            else:
                #! el trabajo no tiene relación con su carrera
                noRelacion += 1

            # * Tiempo en el que están trabajando
            if a.antiguedad == 1:
                a1 += 1
            elif a.antiguedad == 2:
                a2 += 1
            elif a.antiguedad == 3:
                a3 += 1
            else:
                a4 += 1

            # * sector en el que trabaja
            if a.sector == 1:
                s1 += 1
            elif a.sector == 2:
                s2 += 1
            elif a.sector == 3:
                s3 += 1
            else:
                s4 += 1

            # * Puesto en su trabajo
            if a.rol == 1:
                p1 += 1
            elif a.rol == 2:
                p2 += 1
            elif a.rol == 3:
                p3 += 1
            elif a.rol == 4:
                p4 += 1
            elif a.rol == 5:
                p5 += 1
            elif a.rol == 6:
                p6 += 1
            else:
                p7 += 1

            # * medio de conseguir trabajo
            if a.medioTrabajo == 1:
                m1 += 1
            elif a.medioTrabajo == 2:
                m2 += 1
            elif a.medioTrabajo == 3:
                m3 += 1
            elif a.medioTrabajo == 4:
                m4 += 1
            else:
                m5 += 1

            # * grado de satisfacción
            if a.satisfaccion == 1:
                g1 += 1
            elif a.satisfaccion == 2:
                g2 += 1
            elif a.satisfaccion == 3:
                g3 += 1
            elif a.satisfaccion == 3:
                g4 += 1
            else:
                g5 += 1

        #! el egresado no trabaja
        else:
            noTrabaja += 1

    print(f'a1:{p1} a2{p2} a3{p3} a4{a4} p6{p6}')

    return render(request, 'layouts/A2.html', {
        'anexo': True,
        'subtitle': 'SITUACIÓN LABORAL',
        'trabaja': {'si': trabaja, 'no': noTrabaja},  # *si
        'relacion': {'si': relacion, 'no': noRelacion},  # * si
        'antiguedad': {'uno': a1, 'dos': a2, 'tres': a3, 'cuatro': a4},  # *ya
        'trabajoT': {'uno': t1, 'dos': t2, 'tres': t3, },  # * al toke
        'sector': {'uno': s1, 'dos': s2, 'tres': s3, 'cuatro': s4},  # *yes u do
        'puesto': {'uno': p1, 'dos': p2, 'tres': p3, 'cuatro': p4, 'cinco': p5, 'seis': p6, 'siete': p7},#* o
        'area': {'uno': d1, 'dos': d2, 'tres': d3, 'cuatro': d4, 'cinco': d5, 'seis': d6, 'siete': d7},#* a
        'medio': {'uno': m1, 'dos': m2, 'tres': m3, 'cuatro': m4, 'cinco': m5, },#* 
        'satisfaccion': {'uno': g1, 'dos': g2, 'tres': g3, 'cuatro': g4, },
    })
