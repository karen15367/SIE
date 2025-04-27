from django.shortcuts import render

# Create your views here.
def signin(request):
    return render(request, "vistaSignUp.html")

def vericacion(request):
    return render(request, "vistaVerificacionCorreo.html")