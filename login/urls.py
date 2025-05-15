from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('', views.signin),
    path('recuperacion/', views.contrasena),
    path("confirmar/<str:token>/", views.confirm_pwd, name="confirm_pwd"),
]
