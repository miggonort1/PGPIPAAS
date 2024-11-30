from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import admin
from .views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, CreateCheckoutSessionView


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
    path('api/confirmar_compra/', views.confirmar_compra, name='confirmar_compra'),
    path('api/usuario/', views.obtener_datos_usuario, name='obtener_datos_usuario'),
    path('pedido/detalle/', views.detalle_pedido, name='detalle_pedido'),
    path('create_checkout_session', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('success', views.success_view, name='success'),
    path('cancel', views.cancel_view, name='cancel'),
    path('editar_curso/<int:id>/',views.editar_curso,name='editar_curso'),
    path('crear_curso/',views.crear_curso,name='crear_curso'),
    path('borrar_curso/<int:id>/', views.borrar_curso, name='borrar_curso'),
    path('listar_usuarios/',views.listar_usuarios,name='listar_usuarios'),
    path('detalles_usuario/<int:id>/',views.detalles_usuario,name='detalles_usuario'),
    path('borrar_usuario/<int:id>/', views.borrar_usuario, name='borrar_usuario'),
    path('listar_pedidos/',views.listar_pedidos,name='listar_pedidos'),
    path('detalles_pedido/<int:id>/',views.detalles_pedido,name='detalles_pedido'),
    path('borrar_pedido/<int:id>/', views.borrar_pedido, name='borrar_pedido'),
]
