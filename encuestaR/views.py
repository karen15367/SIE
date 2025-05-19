from django.shortcuts import render

from core.models import EncuestaS1, EncuestaS2, EncuestaS3, EncuestaS4, EncuestaS5, EncuestaS3Empresa
from django.http import HttpResponse
import csv

# Create your views here.


def viewEncuesta(request):
    if request.method == 'POST':

        try:
            lista = [
                {'id': 'PERFIL DEL EGRESADO', 'direccion': 'encuestaR/E1'},
                {'id': 'SITUACIÓN LABORAL', 'direccion': 'encuestaR/E2'},
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
    sF =  EncuestaS1.objects.filter(sexo=1).count()
    sM =  EncuestaS1.objects.filter(sexo=0).count()
    
    e1 =  EncuestaS1.objects.filter(estadoCivil=1).count()
    e2 =  EncuestaS1.objects.filter(estadoCivil=2).count()
    
    t1 =  EncuestaS1.objects.filter(titulado=0).count()
    t2 =  EncuestaS1.objects.filter(titulado=1).count()
    
    p1 =  EncuestaS1.objects.filter(titulado=0).count()
    p2 =  EncuestaS1.objects.filter(titulado=1).count()


    return render(request, 'layouts/E1.html', {
        'anexo': False,
        'subtitle': 'PERFIL DEL EGRESADO',
        'sexo': {'si': sF, 'no':sM},
        'estado': {'si': e1, 'no':e2},
        'titulado': {'si': t1, 'no':t2},
        'paquetes': {'si': p1, 'no':p2},
    })
    
def exportarE1(request):
    data = EncuestaS1.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="encuestaE1_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'CURP', 'Sexo', 'Estado civil', 'Titulado', 'Manejo de paquetes'
    ])

    for e in data:
        writer.writerow([
            e.curp,
            'Femenino' if e.sexo == 1 else 'Masculino',
            'Soltero' if e.estadoCivil == 1 else 'Casado',
            'Sí' if e.titulado == 1 else 'No',
            'Sí' if e.manejoPaquetes == 1 else 'No'
        ])

    return response


def viewE2(request):
    c1 =  EncuestaS2.objects.filter(calidadDocentes=1).count()
    c2 =  EncuestaS2.objects.filter(calidadDocentes=2).count()
    c3 =  EncuestaS2.objects.filter(calidadDocentes=3).count()
    c4 =  EncuestaS2.objects.filter(calidadDocentes=4).count()
    
    p1 =  EncuestaS2.objects.filter(planEstudios=1).count()
    p2 =  EncuestaS2.objects.filter(planEstudios=2).count()
    p3 =  EncuestaS2.objects.filter(planEstudios=3).count()
    p4 =  EncuestaS2.objects.filter(planEstudios=4).count()
    
    o1 =  EncuestaS2.objects.filter(oportunidadesProyectos=1).count()
    o2 =  EncuestaS2.objects.filter(oportunidadesProyectos=2).count()
    o3 =  EncuestaS2.objects.filter(oportunidadesProyectos=3).count()
    o4 =  EncuestaS2.objects.filter(oportunidadesProyectos=4).count()
    
    e1 =  EncuestaS2.objects.filter(oportunidadesProyectos=1).count()
    e2 =  EncuestaS2.objects.filter(oportunidadesProyectos=2).count()
    e3 =  EncuestaS2.objects.filter(oportunidadesProyectos=3).count()
    e4 =  EncuestaS2.objects.filter(oportunidadesProyectos=4).count()
    
    s1 =  EncuestaS2.objects.filter(satisfaccionCondiciones=1).count()
    s2 =  EncuestaS2.objects.filter(satisfaccionCondiciones=2).count()
    s3 =  EncuestaS2.objects.filter(satisfaccionCondiciones=3).count()
    s4 =  EncuestaS2.objects.filter(satisfaccionCondiciones=4).count()
    
    x1 =  EncuestaS2.objects.filter(experienciaResidencia=1).count()
    x2 =  EncuestaS2.objects.filter(experienciaResidencia=2).count()
    x3 =  EncuestaS2.objects.filter(experienciaResidencia=3).count()
    x4 =  EncuestaS2.objects.filter(experienciaResidencia=4).count()


    return render(request, 'layouts/E2.html', {
        'anexo': False,
        'subtitle': 'PERTINENCIA Y DISPONIBILIDAD DE MEDIOS Y RECURSOS PARA EL APRENDIZAJE',
        'calidad': {'uno': c1, 'dos': c2, 'tres': c3, 'cuatro': c4},  
        'plan': {'uno': p1, 'dos': p2, 'tres': p3, 'cuatro': p4},  
        'oportunidad': {'uno': o1, 'dos': o2, 'tres': o3, 'cuatro': o4},  
        'enfasis': {'uno': e1, 'dos': e2, 'tres': e3, 'cuatro': e4},  
        'satisfaccion': {'uno': s1, 'dos': s2, 'tres': s3, 'cuatro': s4},  
        'experiencia': {'uno': x1, 'dos': x2, 'tres': x3, 'cuatro': x4},  
        
    })

def exportarE2(request):
    data = EncuestaS2.objects.select_related('folioEncuesta__curp').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="encuestaE2_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'CURP', 'Calidad docentes', 'Plan estudios',
        'Oportunidad en proyectos', 'Énfasis en investigación',
        'Satisfacción condiciones de estudio', 'Experiencia residencia'
    ])

    for e in data:
        writer.writerow([
            e.folioEncuesta.curp.curp,
            e.get_calidadDocentes_display() if e.calidadDocentes else '',
            e.get_planEstudios_display() if e.planEstudios else '',
            e.get_oportunidadesProyectos_display() if e.oportunidadesProyectos else '',
            e.get_enfasisInvestigacion_display() if e.enfasisInvestigacion else '',
            e.get_satisfaccionCondiciones_display() if e.satisfaccionCondiciones else '',
            e.get_experienciaResidencia_display() if e.experienciaResidencia else ''
        ])

    return response

