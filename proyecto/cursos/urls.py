from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('', views.home, name='home'),  # Pantalla de inicio
    path('inicio_sesion/', views.inicioSesion, name='inicioSesion'),  # Formulario de inicio de sesión
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.editar_perfil, name='perfil'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('password_reset/', PasswordResetView.as_view(), name='recuperar_contraseña'),
    path('password_reset_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('buscar_cursos/', views.buscar_cursos, name='buscar_cursos'),
    path('curso/<int:id>/', views.detalle_curso, name='detalle_curso'),
    path('api/carrito/', views.obtener_carrito, name='obtener_carrito'),
    path('api/carrito/agregar/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('api/carrito/eliminar/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
]
