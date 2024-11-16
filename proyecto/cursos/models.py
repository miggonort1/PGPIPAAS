from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    duracion_semanas = models.IntegerField()
    plazas_disponibles = models.IntegerField()
    precio = models.IntegerField()
    imagen = models.CharField(max_length=200, default="https://via.placeholder.com/150")

    departamento = models.CharField(
        max_length=3,
        choices=[
            ('MD', 'Madrid'),
            ('BCN', 'Barcelona'),
            ('VAL', 'Valencia'),
            ('SEV', 'Sevilla'),
            ('ZGZ', 'Zaragoza'),
            ('MAL', 'Málaga'),
            ('BIL', 'Bilbao'),
            ('VLL', 'Valladolid'),
        ],
        default='MD'
    )
    sector_laboral = models.CharField(
        max_length=3,
        choices=[
            ('ADM', 'Administración Pública'),
            ('JUS', 'Justicia'),
            ('SAL', 'Sanidad'),
            ('EDU', 'Educación'),
            ('POL', 'Policía Nacional'),
            ('GUA', 'Guardia Civil'),
            ('BOM', 'Bomberos'),
            ('FIS', 'Fiscalía'),
            ('PRI', 'Prisiones'),
            ('TRA', 'Tráfico'),
        ],
        default='ADM'
    )

    def __str__(self):
        return self.nombre
    
class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre_usuario, password=None, **extra_fields):
        if not correo:
            raise ValueError("El correo es obligatorio")
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre_usuario=nombre_usuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre_usuario, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(correo, nombre_usuario, password, **extra_fields)


class Usuario(AbstractBaseUser):
    correo = models.EmailField(unique=True)
    nombre_usuario = models.CharField(max_length=150, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    direccion_entrega = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=100)
    provincia = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = "nombre_usuario"
    REQUIRED_FIELDS = ["correo"]

    def __str__(self):
        return self.nombre_usuario

class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="carrito")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Carrito de {self.usuario.nombre_usuario}"

class CarritoCurso(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="cursos")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="en_carritos")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        unique_together = ('carrito', 'curso')

    def __str__(self):
        return f"{self.curso.nombre} en {self.carrito.usuario.nombre_usuario}'s carrito"

# Pedido Models
class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ('PEN', 'Pendiente de pago'),
        ('PAG', 'Pagado'),
        ('ENV', 'Enviado'),
        ('ENT', 'Entregado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    estado = models.CharField(max_length=3, choices=ESTADO_PEDIDO, default='PEN', verbose_name="Estado del Pedido")
    direccion_envio = models.CharField(max_length=255, verbose_name="Dirección de Envío")
    ciudad_envio = models.CharField(max_length=100, verbose_name="Ciudad de Envío")
    provincia_envio = models.CharField(max_length=100, verbose_name="Provincia de Envío")
    codigo_postal_envio = models.CharField(max_length=10, verbose_name="Código Postal de Envío")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total del Pedido")

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.nombre_usuario} ({self.estado})"

class PedidoCurso(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="cursos")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="en_pedidos")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")

    def __str__(self):
        return f"{self.cantidad}x {self.curso.nombre} en Pedido {self.pedido.id}"