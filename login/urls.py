from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),             # ← login principal
    path('sign-in/', views.signin, name='signin'),        # ← registro
    path('recuperacion/', views.contrasena, name='recuperacion'),
    path("confirmar/<str:token>/", views.confirm_pwd, name="confirm_pwd"),
    path('recuperacion/', views.contrasena, name='recuperacion'),
    path("confirmar/<str:token>/", views.confirm_pwd, name="confirm_pwd"),
]
