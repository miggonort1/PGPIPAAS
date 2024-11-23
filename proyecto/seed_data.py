import os
import django
from decimal import Decimal
from datetime import datetime
from django.templatetags.static import static

# Configura Django para acceder a los modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proyecto.settings")
django.setup()

from cursos.models import Curso, Usuario, Carrito, CarritoCurso, Pedido, PedidoCurso

# Limpieza de datos previos (opcional)

Curso.objects.all().delete()
Usuario.objects.all().delete()
Carrito.objects.all().delete()
CarritoCurso.objects.all().delete()
Pedido.objects.all().delete()
PedidoCurso.objects.all().delete()

# 15 Cursos con datos específicos
cursos_iniciales = [
    {
        "nombre": "Curso de Policía Nacional",
        "descripcion": "Preparación intensiva para oposiciones a Policía Nacional.",
        "fecha_inicio": "2024-12-20",
        "duracion_semanas": 12,
        "plazas_disponibles": 30,
        "precio": 300,
        "departamento": "MD",
        "sector_laboral": "POL",
        "imagen": "static/images/policia.jpg",
        
    },
    {
        "nombre": "Curso de Bombero",
        "descripcion": "Entrenamiento y teoría para el examen de bombero.",
        "fecha_inicio": "2025-01-15",
        "duracion_semanas": 10,
        "plazas_disponibles": 25,
        "precio": 280,
        "departamento": "BCN",
        "sector_laboral": "BOM",
        "imagen": "static/images/bomberos.jpg",
        
    },
    {
        "nombre": "Curso de Guardia Civil",
        "descripcion": "Formación completa para aspirantes a Guardia Civil.",
        "fecha_inicio": "2025-01-22",
        "duracion_semanas": 14,
        "plazas_disponibles": 35,
        "precio": 350,
        "departamento": "VAL",
        "sector_laboral": "GUA",
        "imagen": "static/images/guardiacivil.jpg",
        
    },
    {
        "nombre": "Curso de Sanidad Pública",
        "descripcion": "Preparación para oposiciones en el sector salud.",
        "fecha_inicio": "2025-02-05",
        "duracion_semanas": 8,
        "plazas_disponibles": 20,
        "precio": 320,
        "departamento": "SEV",
        "sector_laboral": "SAL",
        "imagen": "static/images/sanidadpublica.jpg",
        
    },
    {
        "nombre": "Curso de Justicia Administrativa",
        "descripcion": "Curso intensivo para roles en justicia administrativa.",
        "fecha_inicio": "2025-02-12",
        "duracion_semanas": 16,
        "plazas_disponibles": 30,
        "precio": 450,
        "departamento": "ZGZ",
        "sector_laboral": "JUS",
        "imagen": "static/images/justiciaadministrativa.jpg",
        
    },
    {
        "nombre": "Curso de Educación Primaria",
        "descripcion": "Preparación para oposiciones de maestros de primaria.",
        "fecha_inicio": "2025-02-18",
        "duracion_semanas": 12,
        "plazas_disponibles": 40,
        "precio": 400,
        "departamento": "MAL",
        "sector_laboral": "EDU",
        "imagen": "static/images/educacionprimaria.jpg",
        
    },
    {
        "nombre": "Curso de Fiscal de Hacienda",
        "descripcion": "Curso para aspirantes a fiscal de hacienda.",
        "fecha_inicio": "2025-02-25",
        "duracion_semanas": 14,
        "plazas_disponibles": 15,
        "precio": 500,
        "departamento": "BIL",
        "sector_laboral": "FIS",
        "imagen": "static/images/fiscalhacienda.jpg",
        
    },
    {
        "nombre": "Curso de Administración Pública",
        "descripcion": "Formación para oposiciones en administración pública.",
        "fecha_inicio": "2025-03-01",
        "duracion_semanas": 10,
        "plazas_disponibles": 50,
        "precio": 320,
        "departamento": "VLL",
        "sector_laboral": "ADM",
        "imagen": "static/images/administracionpublica.jpg",
        
    },
    {
        "nombre": "Curso de Informática para Oposiciones",
        "descripcion": "Habilidades informáticas para distintos exámenes de oposición.",
        "fecha_inicio": "2025-03-10",
        "duracion_semanas": 8,
        "plazas_disponibles": 25,
        "precio": 270,
        "departamento": "MD",
        "sector_laboral": "ADM",
        "imagen": "static/images/informatico.jpg",
        
    },
    {
        "nombre": "Curso de Tráfico y Transporte",
        "descripcion": "Preparación para oposiciones de control de tráfico.",
        "fecha_inicio": "2025-03-15",
        "duracion_semanas": 11,
        "plazas_disponibles": 30,
        "precio": 380,
        "departamento": "BCN",
        "sector_laboral": "TRA",
        "imagen": "static/images/traficotransporte.jpg",
        
    },
    {
        "nombre": "Curso de Derecho Administrativo",
        "descripcion": "Formación en derecho administrativo para oposiciones.",
        "fecha_inicio": "2025-03-20",
        "duracion_semanas": 12,
        "plazas_disponibles": 35,
        "precio": 340,
        "departamento": "VAL",
        "sector_laboral": "JUS",
        "imagen": "static/images/derechoadministrativo.jpg",
        
    },
    {
        "nombre": "Curso de Economía Pública",
        "descripcion": "Conocimiento en economía pública para opositores.",
        "fecha_inicio": "2025-03-25",
        "duracion_semanas": 14,
        "plazas_disponibles": 20,
        "precio": 360,
        "departamento": "SEV",
        "sector_laboral": "ADM",
        "imagen": "static/images/economiapublica.jpg",
        
    },
    {
        "nombre": "Curso de Gestión Municipal",
        "descripcion": "Formación en gestión municipal para administración local.",
        "fecha_inicio": "2025-03-30",
        "duracion_semanas": 10,
        "plazas_disponibles": 45,
        "precio": 300,
        "departamento": "ZGZ",
        "sector_laboral": "ADM",
        "imagen": "static/images/gestionmunicipal.jpg",
        
    },
    {
        "nombre": "Curso de Seguridad Social",
        "descripcion": "Curso completo para trabajar en seguridad social.",
        "fecha_inicio": "2025-04-05",
        "duracion_semanas": 15,
        "plazas_disponibles": 30,
        "precio": 380,
        "departamento": "MAL",
        "sector_laboral": "SAL",
        "imagen": "static/images/seguridadsocial.jpg",
        
    },
    {
        "nombre": "Curso de Prisiones",
        "descripcion": "Preparación específica para oposiciones de prisiones.",
        "fecha_inicio": "2025-04-10",
        "duracion_semanas": 9,
        "plazas_disponibles": 25,
        "precio": 330,
        "departamento": "BIL",
        "sector_laboral": "PRI",
        "imagen": "static/images/prisiones.jpg",
    },
]

for curso_data in cursos_iniciales:
    Curso.objects.create(**curso_data)

usuario1 = Usuario.objects.create(
    email="usuario1@example.com",
    nombre_usuario="pgpipaas1",
    nombre="Juan",
    apellido="Pérez",
    direccion_entrega="Calle Falsa 123",
    ciudad="Madrid",
    provincia="Madrid",
    codigo_postal="28001",
    telefono="123456789",
    is_active=True 
)
usuario1.set_password("1234")  # Cifra la contraseña
usuario1.save()  # Guarda los cambios

usuario2 = Usuario.objects.create(
    email="usuario2@example.com",
    nombre_usuario="pgpipaas2",
    nombre="Ana",
    apellido="López",
    direccion_entrega="Avenida Siempre Viva 742",
    ciudad="Barcelona",
    provincia="Barcelona",
    codigo_postal="08001",
    telefono="987654321",
    is_active=True 
)
usuario2.set_password("1234")  # Cifra la contraseña
usuario2.save()  # Guarda los cambios

print("Usuarios añadidos a la base de datos.")

# Crear carrito para usuario1 y añadir dos cursos
carrito_usuario1 = Carrito.objects.create(usuario=usuario1)

# Asumiendo que los cursos ya existen y tomando los dos primeros
curso1 = Curso.objects.get(nombre="Curso de Policía Nacional")
curso2 = Curso.objects.get(nombre="Curso de Bombero")

CarritoCurso.objects.create(carrito=carrito_usuario1, curso=curso1, cantidad=1)
CarritoCurso.objects.create(carrito=carrito_usuario1, curso=curso2, cantidad=1)


# Crear un pedido para usuario1
pedido_usuario1 = Pedido.objects.create(
    usuario=usuario1,
    fecha_creacion=datetime.now(),
    estado="PAG",  # Pedido marcado como "Pagado"
    direccion_envio=usuario1.direccion_entrega,
    ciudad_envio=usuario1.ciudad,
    provincia_envio=usuario1.provincia,
    codigo_postal_envio=usuario1.codigo_postal,
    total=Decimal("580.00")  # Total calculado manualmente como suma de curso1 y curso2
)

# Añadir los mismos cursos del carrito al pedido
PedidoCurso.objects.create(pedido=pedido_usuario1, curso=curso1, cantidad=1, precio_unitario=curso1.precio)
PedidoCurso.objects.create(pedido=pedido_usuario1, curso=curso2, cantidad=1, precio_unitario=curso2.precio)
