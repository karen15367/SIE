# anexoR/forms.py
from django import forms
from core.models import Egresado

class FiltroEncuestaForm(forms.Form):
    SEXO_CHOICES = [('', 'Todos'), ('1', 'Femenino'), ('0', 'Masculino')]
    
    sexo = forms.ChoiceField(choices=SEXO_CHOICES, required=False, 
                            widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Inicializaremos estas opciones en el __init__
    años = forms.ChoiceField(required=False, 
                            widget=forms.Select(attrs={'class': 'form-control'}))
    
    carrera = forms.ChoiceField(required=False, 
                               widget=forms.Select(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obtener años únicos (evitando error si fechaEgreso es None)
        años_egreso = [(str(year), str(year)) 
                      for year in set(egresado.fechaEgreso.year 
                                     for egresado in Egresado.objects.exclude(fechaEgreso=None))]
        años_egreso.sort(reverse=True)  # Ordenar descendente
        self.fields['años'].choices = [('', 'Todos')] + años_egreso
        
        # Obtener carreras únicas
        carreras = [(carrera, carrera) 
                   for carrera in Egresado.objects.values_list('carrera', flat=True).distinct()]
        self.fields['carrera'].choices = [('', 'Todas')] + sorted(carreras)