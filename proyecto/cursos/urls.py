from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Pantalla de inicio
    path('perfil/', views.perfil, name='perfil'),  # Formulario de inicio de sesión
    path('registro/', views.registro, name='registro'),
    
]
