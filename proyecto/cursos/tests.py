import pytest
from cursos.models import Curso, Usuario, Carrito, CarritoCurso, Pedido, PedidoCurso
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.messages import get_messages
from django.utils import timezone
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import JsonResponse
from django.test import Client
import json
import uuid
from decimal import Decimal

UsuarioModel = get_user_model()

@pytest.mark.django_db
def test_creacion_curso():
    """
    Verifica que se pueda crear un curso correctamente.
    """
    curso = Curso.objects.create(
        nombre="Curso de Prueba",
        descripcion="Este es un curso de prueba",
        fecha_inicio=date.today() + timedelta(days=30),
        duracion_semanas=8,
        plazas_disponibles=25,
        precio=300,
        departamento="MD",
        sector_laboral="ADM",
        fabricante="OP",
    )
    assert Curso.objects.count() == 1
    assert curso.nombre == "Curso de Prueba"
    assert curso.departamento == "MD"

@pytest.mark.django_db
def test_creacion_usuario():
    """
    Verifica que se pueda crear un usuario correctamente.
    """
    usuario = UsuarioModel.objects.create_user(
        email="usuario@test.com",
        nombre_usuario="usuario_test",
        password="securepassword",
        nombre="Test",
        apellido="Usuario",
        direccion_entrega="Calle Falsa 123",
        ciudad="Madrid",
        provincia="Madrid",
        codigo_postal="28001",
    )
    assert UsuarioModel.objects.count() == 1
    assert usuario.nombre_usuario == "usuario_test"
    assert usuario.check_password("securepassword")

@pytest.mark.django_db
def test_creacion_carrito():
    """
    Verifica que se pueda asociar un carrito a un usuario.
    """
    usuario = UsuarioModel.objects.create_user(
        email="usuario@test.com",
        nombre_usuario="usuario_test",
        password="securepassword",
    )
    carrito = Carrito.objects.create(usuario=usuario)
    assert carrito.usuario == usuario
    assert str(carrito) == f"Carrito de {usuario.nombre_usuario}"

@pytest.mark.django_db
def test_carrito_curso_relacion():
    """
    Verifica la relación entre Carrito y Curso.
    """
    usuario = UsuarioModel.objects.create_user(
        email="usuario@test.com",
        nombre_usuario="usuario_test",
        password="securepassword",
    )
    carrito = Carrito.objects.create(usuario=usuario)
    curso = Curso.objects.create(
        nombre="Curso de Prueba",
        descripcion="Este es un curso de prueba",
        fecha_inicio=date.today() + timedelta(days=10),
        duracion_semanas=5,
        plazas_disponibles=20,
        precio=150,
    )
    carrito_curso = CarritoCurso.objects.create(carrito=carrito, curso=curso, cantidad=2)
    assert carrito_curso.carrito == carrito
    assert carrito_curso.curso == curso
    assert carrito_curso.cantidad == 2
    assert str(carrito_curso) == f"{curso.nombre} en {usuario.nombre_usuario}'s carrito"

@pytest.mark.django_db
def test_creacion_pedido():
    """
    Verifica que se pueda crear un pedido asociado a un usuario.
    """
    usuario = UsuarioModel.objects.create_user(
        email="usuario@test.com",
        nombre_usuario="usuario_test",
        password="securepassword",
    )
    pedido = Pedido.objects.create(
        usuario=usuario,
        estado="PEN",
        direccion_envio="Calle Real 456",
        ciudad_envio="Madrid",
        provincia_envio="Madrid",
        codigo_postal_envio="28002",
        total=120.50,
    )
    assert Pedido.objects.count() == 1
    assert pedido.usuario == usuario
    assert pedido.estado == "PEN"
    assert pedido.total == 120.50
    assert str(pedido) == f"Pedido {pedido.id} ({pedido.estado})"

@pytest.mark.django_db
def test_pedido_curso_relacion():
    """
    Verifica la relación entre Pedido y Curso.
    """
    usuario = UsuarioModel.objects.create_user(
        email="usuario@test.com",
        nombre_usuario="usuario_test",
        password="securepassword",
    )
    pedido = Pedido.objects.create(usuario=usuario, total=300.00)
    curso = Curso.objects.create(
        nombre="Curso Avanzado",
        descripcion="Curso de nivel avanzado",
        fecha_inicio=date.today(),
        duracion_semanas=12,
        plazas_disponibles=10,
        precio=300,
    )
    pedido_curso = PedidoCurso.objects.create(
        pedido=pedido,
        curso=curso,
        cantidad=1,
        precio_unitario=300,
        email="usuario@test.com",
        nombre="Test User",
    )
    assert pedido_curso.pedido == pedido
    assert pedido_curso.curso == curso
    assert pedido_curso.cantidad == 1
    assert pedido_curso.precio_unitario == 300
    assert str(pedido_curso) == f"1x {curso.nombre} en Pedido {pedido.id}"

@pytest.mark.django_db
class TestInicioSesionView:

    def test_inicio_sesion_usuario_inexistente(self, client):
        """
        Test que verifica el comportamiento cuando se intenta iniciar sesión
        con un email no registrado.
        """
        response = client.post(reverse('inicioSesion'), {
            'email': 'inexistente@test.com',
            'password': 'password123',
        })
        assert response.status_code == 200
        assert "El email no existe." in response.content.decode()

    def test_inicio_sesion_usuario_inactivo(self, client):
        """
        Test que verifica el comportamiento cuando se intenta iniciar sesión
        con un usuario inactivo.
        """
        usuario = Usuario.objects.create_user(
            email='inactivo@test.com',
            nombre_usuario='usuario_inactivo',
            password='password123',
            is_active=False
        )
        response = client.post(reverse('inicioSesion'), {
            'email': usuario.email,
            'password': 'password123',
        })
        assert response.status_code == 200
        assert "Tu cuenta está inactiva. No puedes iniciar sesión." in response.content.decode()

    def test_inicio_sesion_contraseña_incorrecta(self, client):
        """
        Test que verifica el comportamiento cuando se intenta iniciar sesión
        con una contraseña incorrecta.
        """
        usuario = Usuario.objects.create_user(
            email='usuario@test.com',
            nombre_usuario='usuario_activo',
            password='password123'
        )
        response = client.post(reverse('inicioSesion'), {
            'email': usuario.email,
            'password': 'password_incorrecta',
        })
        assert response.status_code == 200
        assert "Contraseña incorrecta." in response.content.decode()

    def test_inicio_sesion_exitoso(self, client):
        """
        Test que verifica el comportamiento cuando el inicio de sesión
        es exitoso.
        """
        usuario = Usuario.objects.create_user(
            email='usuario@test.com',
            nombre_usuario='usuario_activo',
            password='password123'
        )
        response = client.post(reverse('inicioSesion'), {
            'email': usuario.email,
            'password': 'password123',
        })
        assert response.status_code == 302  # Redirige al home
        assert response.url == reverse('home')

    def test_inicio_sesion_metodo_get(self, client):
        """
        Test que verifica que se renderice correctamente la página
        de inicio de sesión al usar el método GET.
        """
        response = client.get(reverse('inicioSesion'))
        assert response.status_code == 200
        assert "Inicio de Sesión" in response.content.decode()

@pytest.mark.django_db
class TestRegistroView:
    def test_registro_get(self, client):
        """
        Test que verifica que se renderice correctamente la página de registro con el método GET.
        """
        response = client.get(reverse('registro'))
        assert response.status_code == 200
        assert "Registro" in response.content.decode()

    def test_registro_exitoso(self, client):
        """
        Test que verifica que el registro sea exitoso con datos válidos.
        """
        data = {
            'email': 'nuevo_usuario@test.com',
            'nombre_usuario': 'nuevo_usuario',
            'password': 'password123',
            'confirm_password': 'password123',  # Confirmación de la contraseña
            'nombre': 'Nuevo',
            'apellido': 'Usuario',
            'direccion_entrega': 'Calle Falsa 123',
            'ciudad': 'Ciudad Test',
            'provincia': 'Provincia Test',
            'codigo_postal': '12345',
        }
        response = client.post(reverse('registro'), data)
        assert response.status_code == 302  # Redirige al home
        assert response.url == reverse('home')  # Verifica que se redirige correctamente
        assert Usuario.objects.filter(email=data['email']).exists()  # Verifica que el usuario se creó

    def test_registro_datos_invalidos(self, client):
        """
        Test que verifica el manejo de errores cuando se envían datos inválidos.
        """
        data = {
            'email': '',  # Email vacío (inválido)
            'nombre_usuario': '',
            'password': '',
        }
        response = client.post(reverse('registro'), data)
        assert response.status_code == 200  # No redirige, muestra el formulario nuevamente
        assert "Por favor corrige los errores en el formulario." in response.content.decode()
        assert not Usuario.objects.filter(email=data['email']).exists()

@pytest.mark.django_db
class TestEditarPerfilView:
    def test_editar_perfil_autenticado_exitoso(self, client):
        """
        Test que verifica que un usuario autenticado pueda editar su perfil correctamente.
        """
        # Crear un usuario de prueba
        user = get_user_model().objects.create_user(
            email='usuario@test.com',
            nombre_usuario='usuario',
            password='password123'
        )

        # Hacer login como el usuario
        client.login(email='usuario@test.com', password='password123')

        # Datos actualizados para el perfil
        data = {
            'nombre': 'Nuevo Nombre',
            'apellido': 'Nuevo Apellido',
            'direccion_entrega': 'Nueva dirección 123',
            'ciudad': 'Nueva Ciudad',
            'provincia': 'Nueva Provincia',
            'codigo_postal': '54321'
        }

        # Realizar el POST para actualizar el perfil
        response = client.post(reverse('perfil'), data)

        # Verificar que la respuesta sea una redirección a la vista de perfil
        assert response.status_code == 302  # Redirección esperada
        user.refresh_from_db()  # Refrescar el usuario desde la base de datos
        assert user.nombre == data['nombre']
        assert user.apellido == data['apellido']
        assert user.direccion_entrega == data['direccion_entrega']
        assert user.ciudad == data['ciudad']
        assert user.provincia == data['provincia']
        assert user.codigo_postal == data['codigo_postal']

    def test_editar_perfil_autenticado_invalid_form(self, client):
        """
        Test que verifica que si el formulario es inválido, se queda en la misma página.
        """
        # Crear un usuario de prueba
        user = get_user_model().objects.create_user(
            email='usuario@test.com', 
            nombre_usuario='usuario', 
            password='password123'
        )
        
        # Hacer login como el usuario
        client.login(email='usuario@test.com', password='password123')

        # Datos inválidos para el perfil (nombre vacío)
        data = {
            'nombre': '',
            'apellido': 'Nuevo Apellido',
            'direccion_entrega': 'Nueva dirección 123',
            'ciudad': 'Nueva Ciudad',
            'provincia': 'Nueva Provincia',
            'codigo_postal': '54321'
        }

        # Realizar el POST con datos inválidos
        response = client.post(reverse('perfil'), data)

        # Verificar que el formulario no se ha guardado y se ha quedado en la misma página
        assert response.status_code == 200  # El formulario debe volver a la misma página
        assert 'form' in response.context  # Verificar que el formulario sigue presente

    def test_editar_perfil_no_autenticado(self, client):
        """
        Test que verifica que un usuario no autenticado sea redirigido al login.
        """
        # Intentar acceder al perfil sin estar autenticado
        response = client.get(reverse('perfil'))

        # Verificar que el usuario no autenticado es redirigido al login
        assert response.status_code == 302  # Redirige
        assert response.url == reverse('inicioSesion')  # Redirige al login

        # Verificar que se muestra el mensaje de error
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 1
        assert str(messages[0]) == "Debes iniciar sesión para acceder a tu perfil."

@pytest.mark.django_db
def test_detalle_curso_existente(client):
    # Crear un curso de prueba
    curso = Curso.objects.create(
        nombre="Curso de Prueba",
        descripcion="Descripción del curso",
        fecha_inicio="2024-01-01",
        duracion_semanas=10,
        plazas_disponibles=20,
        precio=100,
        sector_laboral="ADM",
        fabricante="OP"
    )
    
    # Generar la URL del detalle del curso usando reverse() con el ID del curso
    url = reverse('detalle_curso', kwargs={'id': curso.id})

    # Hacer una solicitud al detalle del curso
    response = client.get(url)

    # Verificar que la respuesta sea correcta (código de estado 200)
    assert response.status_code == 200

    # Verificar que el contenido de la respuesta contiene el nombre del curso
    assert "Curso de Prueba" in response.content.decode()
    assert "Descripción del curso" in response.content.decode()
# Test cuando el curso no existe
@pytest.mark.django_db
def test_detalle_curso_no_existente(client):
    # Intentar acceder a un curso que no existe
    url = reverse('detalle_curso', args=[9999])  # Suponiendo que no existe un curso con este ID

    # Realizar la solicitud GET a la vista
    response = client.get(url)

    # Verificar que la respuesta es 404
    assert response.status_code == 404

@pytest.mark.django_db
def test_cerrar_sesion(client):
    # Crear un usuario de prueba con el email y nombre de usuario
    usuario = get_user_model().objects.create_user(
        email="usuario@test.com",
        nombre_usuario="testuser",  # Este es solo un campo adicional, no el de login
        password="securepassword",
    )

    # Iniciar sesión con el usuario creado (usando el email en lugar de nombre_usuario)
    login_success = client.login(email="usuario@test.com", password="securepassword")
    
    # Verificar que el login fue exitoso
    assert login_success is True

    # Verificar que el usuario esté autenticado antes de cerrar sesión
    response = client.get(reverse('home'))
    assert response.status_code == 200  # Verificamos que la página de inicio se carga correctamente
    assert b"testuser" in response.content  # Verificamos que el nombre de usuario esté en el contenido de la página (usuario autenticado)

    # Realizar la solicitud para cerrar sesión
    response = client.get(reverse('cerrar_sesion'))

    # Verificar que el usuario ha sido desconectado
    assert response.status_code == 302  # Verificar que se redirige (código 302)
    assert response.url == reverse('home')  # Verificar que la redirección es a la página de inicio

    # Verificar que el usuario ya no está autenticado
    response = client.get(reverse('home'))
    assert response.status_code == 200  # La página de inicio debe seguir cargando
    assert b"testuser" not in response.content  # El nombre de usuario no debe aparecer, ya que debería estar desconectado


@pytest.mark.django_db
def test_buscar_cursos(client):
    # Crear algunos cursos de prueba
    Curso.objects.create(nombre="Curso de Python", departamento="IT", sector_laboral="Desarrollo", fabricante="Udemy")
    Curso.objects.create(nombre="Curso de Django", departamento="IT", sector_laboral="Desarrollo", fabricante="Coursera")
    
    # Realizar una búsqueda sin filtros
    response = client.get(reverse('buscar_cursos'))
    assert response.status_code == 200
    assert len(response.context['resultados']) == 2  # Deberían aparecer dos cursos
    
    # Realizar una búsqueda con un término
    response = client.get(reverse('buscar_cursos') + '?q=Python')
    assert response.status_code == 200
    assert len(response.context['resultados']) == 1  # Solo debe aparecer "Curso de Python"
    assert b"Curso de Python" in response.content
    assert b"Curso de Django" not in response.content  # No debe aparecer el curso de Django

    # Realizar una búsqueda con un filtro por departamento
    response = client.get(reverse('buscar_cursos') + '?departamento=IT')
    assert response.status_code == 200
    assert len(response.context['resultados']) == 2  # Ambos cursos deben aparecer

    # Realizar una búsqueda con múltiples filtros
    response = client.get(reverse('buscar_cursos') + '?departamento=IT&sector_laboral=Desarrollo')
    assert response.status_code == 200
    assert len(response.context['resultados']) == 2  # Ambos cursos deben aparecer

@pytest.mark.django_db
def test_buscar_cursos(client):
    # Crear algunos cursos de prueba con todos los campos obligatorios
    Curso.objects.create(
        nombre="Curso de Python", 
        descripcion="Curso introductorio de Python",
        fecha_inicio=timezone.now().date(),  # Agregar una fecha válida
        duracion_semanas=10,
        plazas_disponibles=20,
        precio=100,
        departamento="MD",  # Elige un valor válido para el departamento
        sector_laboral="EDU",  # Elige un valor válido para el sector_laboral
        fabricante="EDX",  # Elige un valor válido para el fabricante
    )
    Curso.objects.create(
        nombre="Curso de Django", 
        descripcion="Curso de desarrollo web con Django",
        fecha_inicio=timezone.now().date(),  # Agregar una fecha válida
        duracion_semanas=8,
        plazas_disponibles=15,
        precio=120,
        departamento="BCN",  # Elige un valor válido para el departamento
        sector_laboral="POL",  # Elige un valor válido para el sector_laboral
        fabricante="US",  # Elige un valor válido para el fabricante
    )

    # Realizar una búsqueda de cursos sin ningún parámetro
    response = client.get(reverse('buscar_cursos'))
    assert response.status_code == 200
    assert "Curso de Python" in response.content.decode()  # Verificar que el curso se muestra en la respuesta
    assert "Curso de Django" in response.content.decode()  # Verificar que el curso se muestra en la respuesta

    # Realizar una búsqueda filtrando por nombre del curso
    response = client.get(reverse('buscar_cursos') + '?q=Python')
    assert response.status_code == 200
    assert "Curso de Python" in response.content.decode()  # Verificar que el curso correcto se muestra
    assert "Curso de Django" not in response.content.decode()  # Verificar que el otro curso no se muestra

    # Filtrar por departamento
    response = client.get(reverse('buscar_cursos') + '?departamento=MD')
    assert response.status_code == 200
    assert "Curso de Python" in response.content.decode()  # Verificar que el curso correspondiente se muestra
    assert "Curso de Django" not in response.content.decode()  # Verificar que el otro curso no se muestra

    # Filtrar por sector laboral
    response = client.get(reverse('buscar_cursos') + '?sector_laboral=EDU')
    assert response.status_code == 200
    assert "Curso de Python" in response.content.decode()  # Verificar que el curso correspondiente se muestra
    assert "Curso de Django" not in response.content.decode()  # Verificar que el otro curso no se muestra

    # Filtrar por fabricante
    response = client.get(reverse('buscar_cursos') + '?fabricante=EDX')
    assert response.status_code == 200
    assert "Curso de Python" in response.content.decode()  # Verificar que el curso correspondiente se muestra
    assert "Curso de Django" not in response.content.decode()  # Verificar que el otro curso no se muestra

@pytest.mark.django_db
def test_obtener_carrito(client):
    # Crear algunos cursos de prueba
    curso1 = Curso.objects.create(
        nombre="Curso de Python",
        descripcion="Curso introductorio de Python",
        fecha_inicio="2024-01-01",
        duracion_semanas=10,
        plazas_disponibles=20,
        precio=100,
        departamento="MD",
        sector_laboral="EDU",
        fabricante="EDX"
    )

    curso2 = Curso.objects.create(
        nombre="Curso de Django",
        descripcion="Curso de desarrollo web con Django",
        fecha_inicio="2024-02-01",
        duracion_semanas=8,
        plazas_disponibles=15,
        precio=120,
        departamento="BCN",
        sector_laboral="POL",
        fabricante="US"
    )

    # Simulamos la adición de cursos al carrito usando la vista 'agregar_al_carrito'
    # Primero, añadir el curso 1 al carrito
    response = client.post(reverse('agregar_al_carrito'), data=json.dumps({'curso_id': curso1.id}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['success'] == True

    # Luego, añadir el curso 2 al carrito
    response = client.post(reverse('agregar_al_carrito'), data=json.dumps({'curso_id': curso2.id}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['success'] == True

    # Ahora verificamos que los cursos están en el carrito a través de la vista 'obtener_carrito'
    response = client.get(reverse('obtener_carrito'))

    # Comprobar que la respuesta es un JsonResponse
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    # Verificar los datos del carrito
    response_data = response.json()

    # Verificar que hay 2 cursos en el carrito
    assert len(response_data['cursos']) == 2

    # Verificar los detalles del primer curso (Curso de Python)
    curso1_data = response_data['cursos'][0]
    assert curso1_data['id'] == str(curso1.id)
    assert curso1_data['nombre'] == curso1.nombre
    assert curso1_data['cantidad'] == 1
    assert curso1_data['precio_unitario'] == (curso1.precio)
    assert curso1_data['precio_total'] == (curso1.precio)

    # Verificar los detalles del segundo curso (Curso de Django)
    curso2_data = response_data['cursos'][1]
    assert curso2_data['id'] == str(curso2.id)
    assert curso2_data['nombre'] == curso2.nombre
    assert curso2_data['cantidad'] == 1
    assert curso2_data['precio_unitario'] == (curso2.precio)
    assert curso2_data['precio_total'] == (curso2.precio)

    # Verificar el precio total
    total_precio = (curso1.precio * 1) + (curso2.precio * 1)
    assert response_data['total_precio'] == (total_precio)

@pytest.mark.django_db
def test_agregar_al_carrito(client):
    # Crear algunos cursos de prueba
    curso1 = Curso.objects.create(
        nombre="Curso de Python",
        descripcion="Curso introductorio de Python",
        fecha_inicio="2024-01-01",
        duracion_semanas=10,
        plazas_disponibles=20,
        precio=100,
        departamento="MD",
        sector_laboral="EDU",
        fabricante="EDX"
    )

    curso2 = Curso.objects.create(
        nombre="Curso de Django",
        descripcion="Curso de desarrollo web con Django",
        fecha_inicio="2024-02-01",
        duracion_semanas=8,
        plazas_disponibles=15,
        precio=120,
        departamento="BCN",
        sector_laboral="POL",
        fabricante="US"
    )

    # Verificar que el carrito está vacío inicialmente
    response = client.get(reverse('obtener_carrito'))
    response_data = response.json()
    assert len(response_data['cursos']) == 0  # El carrito está vacío al principio

    # Añadir el curso 1 al carrito
    response = client.post(reverse('agregar_al_carrito'), data=json.dumps({'curso_id': curso1.id}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['success'] == True
    assert response.json()['message'] == 'Curso añadido al carrito.'

    # Verificar que el carrito tiene el curso 1
    response = client.get(reverse('obtener_carrito'))
    response_data = response.json()
    assert len(response_data['cursos']) == 1
    assert response_data['cursos'][0]['id'] == str(curso1.id)
    assert response_data['cursos'][0]['nombre'] == curso1.nombre
    assert response_data['cursos'][0]['cantidad'] == 1
    assert response_data['cursos'][0]['precio_unitario'] == (curso1.precio)  # Comparar como cadena

    # Añadir el curso 2 al carrito
    response = client.post(reverse('agregar_al_carrito'), data=json.dumps({'curso_id': curso2.id}), content_type='application/json')
    assert response.status_code == 200
    assert response.json()['success'] == True
    assert response.json()['message'] == 'Curso añadido al carrito.'

    # Verificar que el carrito tiene ambos cursos
    response = client.get(reverse('obtener_carrito'))
    response_data = response.json()
    assert len(response_data['cursos']) == 2  # Ahora debe haber 2 cursos en el carrito
    assert response_data['cursos'][1]['id'] == str(curso2.id)
    assert response_data['cursos'][1]['nombre'] == curso2.nombre
    assert response_data['cursos'][1]['cantidad'] == 1
    assert response_data['cursos'][1]['precio_unitario'] == (curso2.precio)  # Comparar como cadena

    # Verificar el precio total
    total_precio = (curso1.precio * 1 + curso2.precio * 1)  # Asegúrate de comparar como cadena
    assert response_data['total_precio'] == total_precio

@pytest.mark.django_db
def test_confirmar_compra(client):
    # Crear un usuario de prueba
    user = get_user_model().objects.create_user(
        email='testuser@example.com', 
        nombre_usuario='testuser', 
        password='testpassword'
    )

    # Crear algunos cursos de prueba
    curso_1 = Curso.objects.create(
        nombre='Curso 1', descripcion='Descripción Curso 1', precio=100,
        fecha_inicio='2024-01-01', duracion_semanas=4, plazas_disponibles=30
    )
    curso_2 = Curso.objects.create(
        nombre='Curso 2', descripcion='Descripción Curso 2', precio=150,
        fecha_inicio='2024-01-01', duracion_semanas=6, plazas_disponibles=25
    )

    # Datos de la solicitud
    data = {
        "nombre_comprador": "Test User",
        "email_comprador": "testuser@example.com",
        "direccion_envio": "Calle Falsa 123",
        "ciudad_envio": "Madrid",
        "provincia_envio": "Madrid",
        "codigo_postal_envio": "28001",
        "payment-method": "cash-on-delivery",
        "course_id-0-0": str(curso_1.id),
        "course_quantity-0-0": 2,
        "email-0-0": "testuser@example.com",
        "name-0-0": "Test User",
        "course_id-1-0": str(curso_2.id),
        "course_quantity-1-0": 1,
        "email-1-0": "testuser@example.com",
        "name-1-0": "Test User",
    }

    # Iniciar sesión como el usuario
    client.login(email='testuser@example.com', password='testpassword')

    # Hacer la solicitud POST a la vista 'confirmar_compra'
    response = client.post(reverse('confirmar_compra'), json.dumps(data), content_type='application/json')

    # Verificar que la respuesta sea 200 OK
    assert response.status_code == 200

    # Obtener los datos de la respuesta
    response_data = response.json()

    # Verificar que la respuesta indique que el pedido se ha creado correctamente
    assert response_data["success"] is True
    assert response_data["message"] == "Pedido creado con éxito."

    # Verificar que el pedido ha sido creado en la base de datos
    pedido = Pedido.objects.get(usuario=user)
    assert pedido.direccion_envio == "Calle Falsa 123"
    assert pedido.ciudad_envio == "Madrid"
    assert pedido.provincia_envio == "Madrid"
    assert pedido.codigo_postal_envio == "28001"
    assert pedido.total == (curso_1.precio * 2 + curso_2.precio * 1)  # Total = 200 + 150

    # Verificar que los cursos se han agregado al pedido
    pedido_cursos = PedidoCurso.objects.filter(pedido=pedido)
    assert pedido_cursos.count() == 2
    assert pedido_cursos.filter(curso=curso_1, cantidad=2).exists()
    assert pedido_cursos.filter(curso=curso_2, cantidad=1).exists()

    # Verificar que el carrito ha sido eliminado de la sesión
    assert 'carrito' not in client.session

@pytest.mark.django_db
def test_obtener_datos_usuario(client):
    # Crear un usuario de prueba
    user = get_user_model().objects.create_user(
        email='testuser@example.com',
        nombre_usuario='testuser',
        password='testpassword',
        direccion_entrega='123 Calle Principal',
        ciudad='Ciudad de prueba',
        provincia='Provincia de prueba',
        codigo_postal='12345'
    )

    # Iniciar sesión como el usuario
    client.login(email='testuser@example.com', password='testpassword')

    # Hacer la solicitud GET a la vista 'obtener_datos_usuario'
    response = client.get(reverse('obtener_datos_usuario'))

    # Verificar que la respuesta sea 200 OK
    assert response.status_code == 200

    # Obtener los datos de la respuesta
    response_data = response.json()

    # Verificar que la respuesta contenga los datos del usuario
    assert 'nombre' in response_data
    assert 'email' in response_data
    assert 'direccion_entrega' in response_data
    assert 'ciudad' in response_data
    assert 'provincia' in response_data
    assert 'codigo_postal' in response_data

    # Verificar que los datos del usuario sean correctos
    assert response_data['nombre'] == user.nombre
    assert response_data['email'] == user.email
    assert response_data['direccion_entrega'] == user.direccion_entrega
    assert response_data['ciudad'] == user.ciudad
    assert response_data['provincia'] == user.provincia
    assert response_data['codigo_postal'] == user.codigo_postal