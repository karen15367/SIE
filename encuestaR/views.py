from django.shortcuts import render

from core.models import EncuestaS1, EncuestaS2, EncuestaS3, EncuestaS4, EncuestaS5, EncuestaS3Empresa
from django.http import HttpResponse
from django.db.models import Count
import csv

# Create your views here.


def viewEncuesta(request):
    lista = [
        {'id': 'PERFIL DEL EGRESADO', 'direccion': 'encuestaR/E1'},
        {'id': 'PERTINENCIA Y DISPONIBILIDAD', 'direccion': 'encuestaR/E2'},
        {'id': 'UBICACIÓN LABORAL', 'direccion': 'encuestaR/E3Empresa'},
        {'id': 'DATOS DE LA EMPRESA/ORGANIZACIÓN', 'direccion': 'encuestaR/E3'},
        {'id': 'DESEMPEÑO PROFESIONAL', 'direccion': 'encuestaR/E4'},
        {'id': 'DESAROLLO PROFESIONAL Y SOCIAL', 'direccion': 'encuestaR/E5'},
    ]

    return render(request, 'respuestasListado.html', {
        'anexo': False,
        'inicio': False,
        'resultado': True,
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


def viewE4(request):

    def contar(campo, choices):
        resultados = EncuestaS4.objects.values(campo).annotate(total=Count(campo))
        
        # Crear un diccionario adaptado para las plantillas
        conteo = {
            '1poco': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5mucho': 0
        }
        
        # Llenar el diccionario con los valores obtenidos
        for r in resultados:
            valor = r[campo]
            if valor == 1:
                conteo['1poco'] = r['total']
            elif valor == 2:
                conteo['2'] = r['total']
            elif valor == 3:
                conteo['3'] = r['total']
            elif valor == 4:
                conteo['4'] = r['total']
            elif valor == 5:
                conteo['5mucho'] = r['total']
        
        return conteo

    context = {
        'areaCampoEstudio': contar('areaCampoEstudio', EncuestaS4.VALORACION_CHOICES),
        'titulacion': contar('titulacion', EncuestaS4.VALORACION_CHOICES),
        'experienciaLaboral': contar('experienciaLaboral', EncuestaS4.VALORACION_CHOICES),
        'competenciaLaboral': contar('competenciaLaboral', EncuestaS4.VALORACION_CHOICES),
        'posicionamientoInstitucion': contar('posicionamientoInstitucion', EncuestaS4.VALORACION_CHOICES),
        'conocimientoIdiomas': contar('conocimientoIdiomas', EncuestaS4.VALORACION_CHOICES),
        'recomendacionesReferencias': contar('recomendacionesReferencias', EncuestaS4.VALORACION_CHOICES),
        'personalidadActitudes': contar('personalidadActitudes', EncuestaS4.VALORACION_CHOICES),
        'capacidadLiderazgo': contar('capacidadLiderazgo', EncuestaS4.VALORACION_CHOICES),
        'otrosAspectos': contar('otrosAspectos', EncuestaS4.VALORACION_CHOICES),
    }

    return render(request, 'layouts/E4.html', context)

def exportarE4(request):
    data = EncuestaS4.objects.select_related('folioEncuesta').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="encuestaE4_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Folio Encuesta',
        'Área o campo de estudio',
        'Titulación',
        'Experiencia laboral',
        'Competencia laboral',
        'Posicionamiento institución',
        'Conocimiento idiomas',
        'Recomendaciones/referencias',
        'Personalidad/actitudes',
        'Capacidad liderazgo',
        'Otros aspectos'
    ])

    for e in data:
        writer.writerow([
            e.folioEncuesta_id,
            e.get_areaCampoEstudio_display() if e.areaCampoEstudio else '',
            e.get_titulacion_display() if e.titulacion else '',
            e.get_experienciaLaboral_display() if e.experienciaLaboral else '',
            e.get_competenciaLaboral_display() if e.competenciaLaboral else '',
            e.get_posicionamientoInstitucion_display() if e.posicionamientoInstitucion else '',
            e.get_conocimientoIdiomas_display() if e.conocimientoIdiomas else '',
            e.get_recomendacionesReferencias_display() if e.recomendacionesReferencias else '',
            e.get_personalidadActitudes_display() if e.personalidadActitudes else '',
            e.get_capacidadLiderazgo_display() if e.capacidadLiderazgo else '',
            e.get_otrosAspectos_display() if e.otrosAspectos else '',
        ])

    return response


def viewE5(request):
    def contar(campo):
        data = EncuestaS5.objects.values(campo).annotate(total=Count(campo))
        return {'Sí': sum(d['total'] for d in data if d[campo] == 1), 'No': sum(d['total'] for d in data if d[campo] == 0)}

    context = {
        'cursosActualizacion': contar('cursosActualizacion'),
        'tomarPosgrado': contar('tomarPosgrado'),
        'orgSociales': contar('perteneceOrganizacionesSociales'),
        'orgProfesionales': contar('perteneceOrganismosProfesionistas'),
        'asociacionEgresados': contar('perteneceAsociacionEgresados'),
    }
    return render(request, 'layouts/E5.html', context)

def exportarE5(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="E5.csv"'
    writer = csv.writer(response)
    writer.writerow(['Folio', 'Cursos Actualización', 'Desea Posgrado', 'Org. Sociales', 'Org. Profesionales', 'Asoc. Egresados'])
    for e in EncuestaS5.objects.all():
        writer.writerow([
            e.folioEncuesta_id,
            e.cursosActualizacion,
            e.tomarPosgrado,
            e.perteneceOrganizacionesSociales,
            e.perteneceOrganismosProfesionistas,
            e.perteneceAsociacionEgresados
        ])
    return response
