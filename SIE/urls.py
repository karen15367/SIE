"""
URL configuration for SIE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#SIE/urls.py
from django.contrib import admin
from django.urls import path, include
from signin import views as signin_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('sign-in/', include('signin.urls')),
    path('index/', include('index.urls') ),
    path('anexo/', include('anexo.urls') ),
    path('admin-signup/', include('signinAdmin.urls')),
    path('encuesta/', include('encuesta.urls') ),
    path('importador/', include('importador.urls')),
    path('anexoR/', include('anexoR.urls') ),
    #path('encuestaR/', include('encuestaR.urls') ),
]
