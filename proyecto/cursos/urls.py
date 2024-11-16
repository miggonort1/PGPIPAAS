from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetView
from .views import CustomPasswordResetDoneView


urlpatterns = [
    path('', views.home, name='home'),  # Pantalla de inicio
    path('inicio_sesion/', views.inicioSesion, name='inicioSesion'),  # Formulario de inicio de sesión
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.editar_perfil, name='perfil'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='recuperar_contrasena'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('buscar_cursos/', views.buscar_cursos, name='buscar_cursos'),
]
