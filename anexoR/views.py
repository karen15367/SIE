from django.shortcuts import render

from django.db.models import Count, Q
from core.models import AnexoS1, AnexoS2, AnexoS3, AnexoS4, Egresado, Encuesta
from .forms import FiltroEncuestaForm
from django.http import HttpResponse
import csv
# Create your views here.


def viewAnexos(request):
    if request.method == 'POST':
        folio = request.POST.get('folio')
        try:
            lista = [
                {'id': 'DATOS GENERALES', 'direccion': 'anexoR/A1'},
                {'id': 'SITUACIÓN LABORAL', 'direccion': 'anexoR/A2'},
                {'id': 'PLAN DE ESTUDIOS / INSTITUCIÓN ', 'direccion': 'anexoR/A3'},
                {'id': 'DESEMPEÑO LABORAL', 'direccion': 'anexoR/A4'},
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

def exportarA1(request):
    data = AnexoS1.objects.select_related('folioEncuesta__curp').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="anexoA1_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['CURP', 'Nombre', 'Correo', 'Sexo', 'Carrera', 'Fecha Egreso', 'Titulado'])

    for a in data:
        egresado = a.folioEncuesta.curp
        writer.writerow([
            egresado.curp,
            a.nombreCompleto or '',
            a.correo or '',
            'Femenino' if egresado.sexo == 1 else 'Masculino',
            egresado.carrera or '',
            a.fechaEgreso or '',
            'Sí' if a.titulado == 1 else 'No'
        ])

    return response


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
            else:
                g4 += 1

        #! el egresado no trabaja
        else:
            noTrabaja += 1

    return render(request, 'layouts/A2.html', {
        'anexo': True,
        'subtitle': 'SITUACIÓN LABORAL',
        'trabaja': {'si': trabaja, 'no': noTrabaja},  # *si
        'relacion': {'si': relacion, 'no': noRelacion},  # * si
        'antiguedad': {'uno': a1, 'dos': a2, 'tres': a3, 'cuatro': a4},  # *ya
        'trabajoT': {'uno': t1, 'dos': t2, 'tres': t3, },  # * al toke
        'sector': {'uno': s1, 'dos': s2, 'tres': s3, 'cuatro': s4},  # *yes u do
        'puesto': {'uno': p1, 'dos': p2, 'tres': p3, 'cuatro': p4, 'cinco': p5, 'seis': p6, 'siete': p7},
        'area': {'uno': d1, 'dos': d2, 'tres': d3, 'cuatro': d4, 'cinco': d5, 'seis': d6, 'siete': d7},
        'medio': {'uno': m1, 'dos': m2, 'tres': m3, 'cuatro': m4, 'cinco': m5, },  # *
        'satisfaccion': {'uno': g1, 'dos': g2, 'tres': g3, 'cuatro': g4, },
    })

def exportarA2(request):
    data = AnexoS1.objects.select_related('folioEncuesta__curp').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="anexoA2_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['CURP', 'Titulado', 'Razón No Título', 'Otra Razón'])

    for a in data:
        egresado = a.folioEncuesta.curp
        writer.writerow([
            egresado.curp,
            'Sí' if a.titulado == 1 else 'No',
            a.get_razonNoTitulo_display() if a.razonNoTitulo else '',
            a.razonNoTituloOtra or ''
        ])

    return response



def viewA3(request):
    answer = AnexoS3.objects.all()

    c1 = c2 = c3 = c4 = 0

    g1 = g2 = g3 = g4 = 0

    r1 = r2 = r3 = r4 = r5 = 0

    a1 = a2 = 0

    i1 = i2 = 0

    p1 = p2 = p3 = p4 = p5 = p6 = p7 = 0

    for a in answer:
        if a.competencias == 1:
            c1 += 1
        elif a.competencias == 2:
            c2 += 1
        elif a.competencias == 3:
            c3 += 1
        else:
            c4 += 1

        # * grado de satisfacción
        if a.satisfaccion == 1:
            g1 += 1
        elif a.satisfaccion == 2:
            g2 += 1
        elif a.satisfaccion == 3:
            g3 += 1
        else:
            g4 += 1

        if a.educativo == 1:
            r1 += 1
        elif a.educativo == 2:
            r2 += 1
        elif a.educativo == 3:
            r3 += 1
        elif a.educativo == 4:
            r4 += 1
        else:
            r5 += 1

        if a.contacto == 1:
            a1 += 1
        else:
            a2 += 1

        if a.participar == 1:
            i1 += 1
            if a.aporte == 1:
                p1 += 1
            elif a.aporte == 2:
                p2 += 1
            elif a.aporte == 3:
                p3 += 1
            elif a.aporte == 4:
                p4 += 1
            elif a.aporte == 5:
                p5 += 1
            elif a.aporte == 6:
                p6 += 1
            else:
                p7 += 1

        else:
            i2 += 1

    return render(request, 'layouts/A3.html', {
        'anexo': True,
        'subtitle': 'PLAN DE ESTUDIOS / INSTITUCIÓN',
        'competencias': {'uno': c1, 'dos': c2, 'tres': c3, 'cuatro': c4},
        'satisfaccion': {'uno': g1, 'dos': g2, 'tres': g3, 'cuatro': g4, },
        'reforzar': {'uno': r1, 'dos': r2, 'tres': r3, 'cuatro': r4, 'cinco': r5},
        'contacto': {'si': a1, 'no': a2},
        'participar': {'si': i1, 'no': i2},
        'aporte': {'uno': p1, 'dos': p2, 'tres': p3, 'cuatro': p4, 'cinco': p5, 'seis': p6, 'siete': p7},

    })

def exportarA3(request):
    data = AnexoS1.objects.select_related('folioEncuesta__curp').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="anexoA3_export.csv"'

    writer = csv.writer(response)
    writer.writerow(['CURP', 'Nombre completo', 'Teléfono', 'Correo', 'Redes sociales'])

    for a in data:
        egresado = a.folioEncuesta.curp
        writer.writerow([
            egresado.curp,
            a.nombreCompleto or '',
            a.telefono or '',
            a.correo or '',
            a.redesSociales or ''
        ])

    return response

def viewA4(request):
    answer = AnexoS4.objects.all()

    h1 = h2 = h3 = h4 = h5 = 0

    c1 = c2 = 0

    d1 = d2 = d3 = d4 = d5 = 0

    r1 = r2 = 0

    z1 = z2 = 0

    s1 = s2 = s3 = s4 = s5 = 0

    i1 = i2 = i3 = i4 = i5 = 0

    p1 = p2 = 0

    w1 = w2 = w3 = w4 = w5 = 0

    g1 = g2 = g3 = g4 = 0

    a1 = a2 = 0

    v1 = v2 = v3 = v4 = v5 = 0

    for a in answer:

        if a.herramientas == 1:
            h1 += 1
        elif a.herramientas == 2:
            h2 += 1
        elif a.herramientas == 3:
            h3 += 1
        elif a.herramientas == 4:
            h4 += 1
        else:
            h5 += 1

        if a.colabora == 1:
            c1 += 1
            if a.tipoInvestigacion == 1:
                d1 += 1
            elif a.tipoInvestigacion == 2:
                d2 += 1
            elif a.tipoInvestigacion == 3:
                d3 += 1
            elif a.tipoInvestigacion == 4:
                d4 += 1
            else:
                d5 += 1
        else:
            c2 += 1

        if a.participaRedes:
            r1 += 1
        else:
            r2 += 1

        if a.certificacion:
            z1 += 1
        else:
            z2 += 1

        if a.servicios == 1:
            s1 += 1
        elif a.servicios == 2:
            s2 += 1
        elif a.servicios == 3:
            s3 += 1
        elif a.servicios == 4:
            s4 += 1
        else:
            s5 += 1

        if a.idiomas == 1:
            i1 += 1
        elif a.idiomas == 2:
            i2 += 1
        elif a.idiomas == 3:
            i3 += 1
        elif a.idiomas == 4:
            i4 += 1
        else:
            i5 += 1

        if a.publicacion:
            p1 += 1
        else:
            p2 += 1

        if a.documentos == 1:
            w1 += 1
        elif a.documentos == 2:
            w2 += 1
        elif a.documentos == 3:
            w3 += 1
        elif a.documentos == 4:
            w4 += 1
        else:
            w5 += 1

        if a.calidad == 1:
            g1 += 1
        elif a.calidad == 2:
            g2 += 1
        elif a.calidad == 3:
            g3 += 1
        else:
            g4 += 1

        if a.asociacion:
            a1 += 1
        else:
            a2 += 1

        if a.etica == 1:
            v1 += 1
        elif a.etica == 2:
            v2 += 1
        elif a.etica == 3:
            v3 += 1
        elif a.etica == 4:
            v4 += 1
        else:
            v5 += 1

    return render(request, 'layouts/A4.html', {
        'anexo': True,
        'subtitle': 'DESEMPEÑO LABORAL',
        'utiliza': {'uno': h1, 'dos': h2, 'tres': h3, 'cuatro': h4, 'cinco': h5},
        'colabora': {'si': c1, 'no': c2},
        'tipo': {'uno': d1, 'dos': d2, 'tres': d3, 'cuatro': d4, 'cinco': d5},
        'redes': {'si': r1, 'no': r2},
        'certificacion': {'si': z1, 'no': z2},
        'servicio': {'uno': s1, 'dos': s2, 'tres': s3, 'cuatro': s4, 'cinco': s5},
        'idiomas': {'uno': i1, 'dos': i2, 'tres': i3, 'cuatro': i4, 'cinco': i5},
        'publicacion': {'si': p1, 'no': p2},
        'documentos': {'uno': w1, 'dos': w2, 'tres': w3, 'cuatro': w4, 'cinco': w5},
        'gestion': {'uno': g1, 'dos': g2, 'tres': g3, 'cuatro': g4},
        'asociacion': {'si': a1, 'no': a2},
        'etica': {'uno': v1, 'dos': v2, 'tres': v3, 'cuatro': v4, 'cinco': v5},

    })
