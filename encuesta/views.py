from django.shortcuts import render

# Create your views here.


def e1(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, "encuesta1.html")


def e2(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, "encuesta2.html")


def e3(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, "encuesta3.html")


def e4(request):
    return render(request, "encuesta4.html")


def e5(request):
    return render(request, "encuesta5.html")


def e5(request):
    return render(request, "encuesta5.html")


def e6(request):
    return render(request, "encuesta6.html")


def e7(request):
    return render(request, "encuesta7.html")


def e8(request):
    return render(request, "encuesta8.html")


def e9(request):
    return render(request, "encuesta9.html")


def e10(request):
    return render(request, "encuesta10.html")


def e11(request):
    return render(request, "encuesta11.html")


def e12(request):
    return render(request, "encuesta12.html")
