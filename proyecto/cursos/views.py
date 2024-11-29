# views.py
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm, CursoForm
from cursos.models import Usuario
from .forms import PerfilForm
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetDoneView
from datetime import date
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.db.models import F
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.http import JsonResponse
from .models import Carrito, CarritoCurso
from django.http import JsonResponse
import json
import uuid
from django.utils import timezone
from decimal import Decimal
from django.views import View
from django.views.generic import TemplateView
from django.conf import settings
import stripe
from django.core.mail import send_mail


def home(request):
    # Obtener todos los cursos
    cursos = Curso.objects.all()

    # Filtros de cursos
    hoy = date.today()
    cursos_pronto = cursos.filter(fecha_inicio__gte=hoy).order_by('fecha_inicio')
    cursos_pocas_plazas = cursos.filter(plazas_disponibles__gt=0 ,plazas_disponibles__lt=20 ).order_by('plazas_disponibles')
    cursos_baratos = cursos.filter(precio__lt=220).order_by('precio')

    # Obtener el orden y dirección (ascendente/descendente)
    orden = request.GET.get('orden', '')  # Obtener el campo de ordenamiento
    direccion = request.GET.get('direccion', 'asc')  # Obtener la dirección de orden (ascendente por defecto)

    if orden == 'fecha':
        if direccion == 'asc':
            cursos_pronto = cursos_pronto.order_by('fecha_inicio')
            cursos_pocas_plazas = cursos_pocas_plazas.order_by('fecha_inicio')
            cursos_baratos = cursos_baratos.order_by('fecha_inicio')
        elif direccion == 'desc':
            cursos_pronto = cursos_pronto.order_by('-fecha_inicio')
            cursos_pocas_plazas = cursos_pocas_plazas.order_by('-fecha_inicio')
            cursos_baratos = cursos_baratos.order_by('-fecha_inicio')
    elif orden == 'precio':
        if direccion == 'asc':
            cursos_pronto = cursos_pronto.order_by('precio')
            cursos_pocas_plazas = cursos_pocas_plazas.order_by('precio')
            cursos_baratos = cursos_baratos.order_by('precio')
        elif direccion == 'desc':
            cursos_pronto = cursos_pronto.order_by('-precio')
            cursos_pocas_plazas = cursos_pocas_plazas.order_by('-precio')
            cursos_baratos = cursos_baratos.order_by('-precio')
    elif orden == 'plazas':
        if direccion == 'asc':
            cursos_pronto = cursos_pronto.order_by('plazas_disponibles')
            cursos_pocas_plazas = cursos_pocas_plazas.order_by('plazas_disponibles')
            cursos_baratos = cursos_baratos.order_by('plazas_disponibles')
        elif direccion == 'desc':
            cursos_pronto = cursos_pronto.order_by('-plazas_disponibles')
            cursos_pocas_plazas = cursos_pocas_plazas.order_by('-plazas_disponibles')
            cursos_baratos = cursos_baratos.order_by('-plazas_disponibles')

    # Paginación de los cursos
    pagina = request.GET.get('page', 1)  # Obtener la página actual (por defecto la 1)
    paginator_pronto = Paginator(cursos_pronto, 6)  # 6 cursos por página
    paginator_pocas_plazas = Paginator(cursos_pocas_plazas, 6)
    paginator_baratos = Paginator(cursos_baratos, 6)

    try:
        cursos_pronto_pag = paginator_pronto.page(pagina)
    except:
        cursos_pronto_pag = paginator_pronto.page(1)

    try:
        cursos_pocas_plazas_pag = paginator_pocas_plazas.page(pagina)
    except:
        cursos_pocas_plazas_pag = paginator_pocas_plazas.page(1)

    try:
        cursos_baratos_pag = paginator_baratos.page(pagina)
    except:
        cursos_baratos_pag = paginator_baratos.page(1)

    # Pasar los cursos al contexto de la plantilla
    context = {
        'cursos_pronto': cursos_pronto_pag,
        'cursos_pocas_plazas': cursos_pocas_plazas_pag,
        'cursos_baratos': cursos_baratos_pag,
        'orden': orden,  # Pasar el filtro de orden
        'direccion': direccion,  # Pasar la dirección de orden
    }

    return render(request, 'cursos/home.html', context)
    
def inicioSesion(request):
    messages.get_messages(request).used = True
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is None:
            # Si 'authenticate' devuelve None, significa que las credenciales no son correctas
            try:
                # Intentamos obtener al usuario de la base de datos para dar mensajes más específicos
                usuario = Usuario.objects.get(email=email)
                if not usuario.is_active:
                    # Si el usuario está inactivo, agregamos un mensaje
                    messages.error(request, "Tu cuenta está inactiva. No puedes iniciar sesión.")
                else:
                    # Si el nombre de usuario existe pero la contraseña es incorrecta
                    messages.error(request, "Contraseña incorrecta.")
            except Usuario.DoesNotExist:
                # Si el usuario no existe, agregamos un mensaje
                messages.error(request, "El email no existe.")
        else:
            # Si la autenticación fue exitosa
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.nombre_usuario}!")
            return redirect('home')  # Redirigir al inicio después de iniciar sesión
    
    return render(request, 'cursos/inicio_sesion.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
            print(form.errors)  # Imprimir errores para depuración
    else:
        form = RegistroUsuarioForm()

    return render(request, 'cursos/registro.html', {'form': form})

def editar_perfil(request):
    if request.user.is_authenticated:
        user = request.user  # Obtén el usuario autenticado
        if request.method == 'POST':
            # Si el formulario se envía (POST), procesar la actualización
            form = PerfilForm(request.POST, instance=user)
            if form.is_valid():
                form.save()  # Guardar los cambios
                messages.success(request, "Tu perfil ha sido actualizado correctamente.")
                return redirect('perfil')  # Redirige al perfil después de actualizar
        else:
            # Si la solicitud es GET, mostrar el formulario con los datos actuales del usuario
            form = PerfilForm(instance=user)

        return render(request, 'cursos/perfil.html', {'form': form})

    else:
        if not messages.get_messages(request):
            # Asegurarse de que no se agregue el mensaje de error si ya está en la sesión
            messages.error(request, "Debes iniciar sesión para acceder a tu perfil.")
        return redirect('inicioSesion')  

def es_admin(user):
    return user.is_superuser

@user_passes_test(es_admin)
def editar_curso(request, id):
    # Obtener el curso que se va a editar
    curso = get_object_or_404(Curso, id=id)
    
    if request.method == 'POST':
        # Procesar el formulario enviado
        form = CursoForm(request.POST, request.FILES, instance=curso)  # Incluye request.FILES si el curso tiene imágenes
        if form.is_valid():
            form.save()  # Guardar cambios en la base de datos
            messages.success(request, f"El curso '{curso.nombre}' ha sido actualizado correctamente.")
            return redirect('detalle_curso', id=curso.id)  # Redirige a la página de detalles del curso
    else:
        # Mostrar el formulario con los datos actuales del curso
        form = CursoForm(instance=curso)
    return render(request, 'cursos/editar_curso.html', {'form': form, 'curso': curso})# Redirige a la página de inicio de sesión (ajusta la URL según corresponda)

@user_passes_test(es_admin)
def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save()
            messages.success(request, f"El curso '{curso.nombre}' ha sido creado exitosamente.")
            return redirect('detalle_curso', id=curso.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = CursoForm()

    return render(request, 'cursos/crear_curso.html', {'form': form})

@user_passes_test(es_admin)
def borrar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    curso_nombre = curso.nombre  # Guardar el nombre antes de borrarlo para mostrar en el mensaje
    curso.delete()
    messages.success(request, f"El curso '{curso_nombre}' ha sido eliminado correctamente.")
    return redirect('home')  # Redirige a la lista de cursos después de eliminar
    
@user_passes_test(es_admin)
def borrar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    nombre = usuario.nombre_usuario  # Guardar el nombre antes de borrarlo para mostrar en el mensaje
    usuario.delete()
    messages.success(request, f"El usuario '{nombre}' ha sido eliminado correctamente.")
    return redirect('listar_usuarios')  # Redirige a la lista de cursos después de eliminar    
    
@user_passes_test(es_admin)
def listar_usuarios(request):
    usuarios = Usuario.objects.all()  # Obtenemos todos los pedidos
    context = {'usuarios': usuarios}  # Definimos el contexto
    return render(request, 'cursos/listar_usuarios.html', context)
    
def detalle_curso(request, id):
    # Obtener el curso o devolver un 404 si no existe
    curso = get_object_or_404(Curso, id=id)
    return render(request, 'cursos/detalle_curso.html', {'curso': curso})

def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('home')  # Redirige a la página de inicio después de cerrar sesión

def buscar_cursos(request):
    query = request.GET.get('q', '')
    departamento = request.GET.get('departamento', '')
    sector_laboral = request.GET.get('sector_laboral', '')
    fabricante = request.GET.get('fabricante', '')
    
    # Si no se proporciona una búsqueda (query vacío), obtener todos los cursos
    resultados = Curso.objects.all()

    if query:
        resultados = Curso.objects.filter(nombre__icontains=query)

    if departamento:
        resultados = resultados.filter(departamento=departamento)

    if sector_laboral:
        resultados = resultados.filter(sector_laboral=sector_laboral)
    
    if fabricante:
        resultados = resultados.filter(fabricante=fabricante)
    return render(request, 'cursos/buscar_cursos.html', {'query': query, 'resultados': resultados, 'departamento_choices': Curso.DEPARTAMENTO_CHOICES,
        'sector_laboral_choices': Curso.SECTOR_LABORAL_CHOICES, 'fabricante_choices': Curso.FABRICANTE_CHOICES,})

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'cursos/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'cursos/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'cursos/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'cursos/password_reset_complete.html'






def obtener_carrito(request):
    # Obtener el carrito desde la sesión
    carrito = request.session.get("carrito", {})
    
    # Calcular los totales y estructurar los datos
    cursos = []
    total_precio = 0
    for curso_id, detalles in carrito.items():
        try:
            curso = Curso.objects.get(id=curso_id)
            precio_total = curso.precio * detalles["cantidad"]
            cursos.append({
                "id": curso_id,
                "nombre": curso.nombre,
                "cantidad": detalles["cantidad"],
                "precio_unitario": curso.precio,
                "precio_total": precio_total,
            })
            total_precio += precio_total
        except Curso.DoesNotExist:
            continue

    data = {
        "cursos": cursos,
        "total_precio": total_precio,
    }
    return JsonResponse(data)

def agregar_al_carrito(request):
    if request.method == 'POST':
        # Parsear datos de la solicitud
        data = json.loads(request.body)
        curso_id = data.get('curso_id')
        cantidad = int(data.get('cantidad'))

        # Obtener el carrito desde la sesión
        carrito = request.session.get('carrito', {})

        # Si el carrito no existe, crear uno vacío
        if not carrito:
            carrito = {}

        # Obtener el curso y añadirlo al carrito
        try:
            curso = Curso.objects.get(id=curso_id)
            
            # Verificar si la cantidad solicitada no supera las plazas disponibles
            if cantidad <= curso.plazas_disponibles:
                # Si el curso ya está en el carrito, incrementar la cantidad
                if curso_id in carrito:
                    if (curso.plazas_disponibles - carrito[curso_id]['cantidad']) >= cantidad:
                        carrito[curso_id]['cantidad'] += cantidad
                    else:
                        return JsonResponse({'success': False, 'message': 'No hay suficientes plazas disponibles'}, status=405)
                else:
                    carrito[curso_id] = {
                        'nombre': curso.nombre,
                        'precio': str(curso.precio),  # Convertir el precio a string por seguridad en JSON
                        'cantidad': cantidad
                    }

                # Guardar el carrito en la sesión
                request.session['carrito'] = carrito

                return JsonResponse({'success': True, 'message': f'{cantidad} curso(s) añadido(s) al carrito.'})
            else:
                return JsonResponse({'success': False, 'message': 'No hay suficientes plazas disponibles'}, status=405)

        except Curso.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Curso no encontrado.'}, status=404)

    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)
def eliminar_del_carrito(request):
    
    if request.method == "DELETE":
        # Obtener el carrito desde la sesión
        carrito = request.session.get('carrito', {})
        # Cargar los datos enviados en el cuerpo de la solicitud (DELETE)
        data = json.loads(request.body)
        curso_id = data.get('curso_id')
        # Verificar si el carrito existe y si el curso_id está presente en el carrito
        if not carrito or curso_id not in carrito:
            return JsonResponse({"success": False, "message": "Curso no encontrado en el carrito."}, status=404)

        # Obtener los detalles del curso
        curso = Curso.objects.get(id=curso_id)
        
        # Verificar si hay más de una unidad del curso
        if carrito[curso_id]['cantidad'] > 1:
            # Reducir la cantidad en 1
            carrito[curso_id]['cantidad'] -= 1
        else:
            # Si la cantidad es 1, eliminar el curso del carrito
            del carrito[curso_id]

        # Guardar el carrito actualizado en la sesión
        request.session['carrito'] = carrito

        return JsonResponse({"success": True, "message": "Curso eliminado del carrito."})

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)
def obtener_o_crear_carrito(request):
    if request.user.is_authenticated:
        carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    else:
        session_id = request.session.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session["session_id"] = session_id
        carrito, creado = Carrito.objects.get_or_create(session_id=session_id)
    return JsonResponse({"carrito_id": carrito.id, "creado": creado})

def finalizar_compra(request):
    # Obtener el carrito desde la sesión
    carrito = request.session.get("carrito", {})

    # Calcular los totales y estructurar los datos
    cursos = []
    total_precio = 0

    for curso_id, detalles in carrito.items():
        try:
            curso = Curso.objects.get(id=curso_id)
            precio_total = curso.precio * detalles["cantidad"]
            cursos.append({
                "id": curso_id,
                "nombre": curso.nombre,
                "cantidad": detalles["cantidad"],
                "precio_unitario": curso.precio,
                "precio_total": precio_total,
            })
            total_precio += precio_total
        except Curso.DoesNotExist:
            continue

    context = {
        "cursos": cursos,
        "total_precio": total_precio,
    }
    
    return render(request, "cursos/finalizar_compra.html", context)

def confirmar_compra(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8')) # Verifica si los datos se reciben correctamente
            print("Datos recibidos:", data) 
            # Extraer los datos necesarios
            
            # Calcula el total (sumar precios de cursos)
            total = 0
            cursos = []
            datos = data['data'] if 'data' in data else data

             # Extraer datos generales
            nombre_comprador = datos.get("nombre_comprador")
            email_comprador = datos.get("email_comprador")
            direccion_envio = datos.get("direccion_envio")
            ciudad_envio = datos.get("ciudad_envio")
            provincia_envio = datos.get("provincia_envio")
            codigo_postal_envio = datos.get("codigo_postal_envio")
            payment_method = datos.get("payment_method")
            items = datos.get("items", [])

            for item in items:
                course_id = int(item['curso_id'])
                course_quantity = int(item['cantidad'])
                
                # Obtener el curso desde la base de datos
                course = Curso.objects.get(id=course_id)
                total += (course.precio * course_quantity)  # Calcular el total
                nombre = item['nombre']
                email = item['email']
                cursos.append({
                    'course': course,
                    'quantity': course_quantity,
                    'precio_unitario': course.precio,
                    'nombre': nombre,  # Usamos el nombre general del comprador
                    'email': email,    # Usamos el email general del comprador
                })
            codigo_seguimiento = str(uuid.uuid4())

            print("funciona 1")
            # Crear el pedido principal
            pedido = Pedido.objects.create(
                usuario=request.user if request.user.is_authenticated else None, # No asociamos un usuario
                direccion_envio=direccion_envio,  # Dejar vacío si no es obligatorio
                ciudad_envio=ciudad_envio,
                provincia_envio=provincia_envio,
                codigo_postal_envio=codigo_postal_envio,
                total=total, # Total vacío
                estado= 'PEN' if payment_method == "cash-on-delivery" else 'PAG',
                fecha_creacion=timezone.now(), # Fecha de creación actual
                codigo_seguimiento=codigo_seguimiento
            )
            
            
            print("funciona 2")
            for curso in cursos:
                PedidoCurso.objects.create(
                    pedido=pedido,
                    curso=curso['course'],  # Curso asociado al pedido
                    cantidad=curso['quantity'],
                    precio_unitario=curso['precio_unitario'],
                    email=curso['email'],
                    nombre=curso['nombre']
                )
            if 'carrito' in request.session:
                del request.session['carrito']  # Eliminar carrito de la sesión
            request.session['ultimo_pedido_id'] = pedido.id
            print(pedido.id)
            print("asdasd")
            return JsonResponse({"success": True, "message": "Pedido creado con éxito."})

        except Exception as e:
            # Capturar cualquier error y devolverlo como respuesta
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    # Si no es un método POST, devolver error 405 (Método no permitido)
    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)
def obtener_datos_usuario(request):
    user = request.user
    return JsonResponse({
        "nombre": user.nombre,
        "email": user.email,
        "direccion_entrega": user.direccion_entrega,
        "ciudad": user.ciudad,
        "provincia": user.provincia,
        "codigo_postal": user.codigo_postal,
    })


def detalle_pedido(request):
    codigo_seguimiento = request.GET.get('codigo_seguimiento')
    
    if not codigo_seguimiento:
        return render(request, 'cursos/pedido_detalle.html', {'error': 'Por favor, introduce un código de seguimiento válido.'})
    
    try:
        pedido = Pedido.objects.get(codigo_seguimiento=codigo_seguimiento)
    except Pedido.DoesNotExist:
        return render(request, 'cursos/pedido_detalle.html', {'error': 'Pedido no encontrado. Verifica el código de seguimiento.'})
    
    return render(request, 'cursos/pedido_detalle.html', {'pedido': pedido})



#---------------------------------- STRIPE ----------------------------------


stripe.api_key = settings.STRIPE_API_KEY

YOUR_DOMAIN = 'http://127.0.0.1:8000'

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):  # Cambiar create_checkout_session por post
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            items = data['data']['items']
            line_items = []
            for item in items:
                curso_id = item.get("curso_id")
                cantidad = item.get("cantidad",1)
            
                curso = Curso.objects.get(id=curso_id)
            
                line_items.append({
                    'price': curso.price_id,
                    'quantity': cantidad,
                })

            checkout_session = stripe.checkout.Session.create(
                line_items= line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + '/success',
                cancel_url=YOUR_DOMAIN + '/cancel',
            )
            confirmar_compra(request)
            

            return JsonResponse({'url': checkout_session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def success_view(request):
    # Recuperar el ID del último pedido desde la sesión
    pedido_id = request.session.get('ultimo_pedido_id')
    ultimo_pedido = None

    if pedido_id:
        # Intentar recuperar el pedido
        ultimo_pedido = get_object_or_404(Pedido, id=pedido_id)

        # Enviar un correo con los detalles del pedido
        if ultimo_pedido:
            try:
                # Enviar un correo a cada persona asociada a un curso
                for curso_pedido in ultimo_pedido.cursos.all():
                    curso_obj = curso_pedido.curso
                    if curso_obj.plazas_disponibles > 0:  # Asegurarse de no tener stock negativo
                        curso_obj.plazas_disponibles -= curso_pedido.cantidad
                        curso_obj.save()
                    subject = f"Detalles de tu curso comprado en el pedido #{ultimo_pedido.id}"
                    recipient_email = curso_pedido.email

                    # Mensaje personalizado por curso
                    message = f"""
                    Hola {curso_pedido.nombre},

                    Gracias por tu compra. Aquí tienes los detalles de tu curso:

                    Curso: {curso_pedido.curso.nombre}
                    Cantidad: {curso_pedido.cantidad}
                    Precio Unitario: {curso_pedido.precio_unitario}€

                    Dirección de Envío:
                    {ultimo_pedido.direccion_envio}
                    {ultimo_pedido.ciudad_envio}, {ultimo_pedido.provincia_envio} {ultimo_pedido.codigo_postal_envio}

                    Código de Seguimiento del Pedido: {ultimo_pedido.codigo_seguimiento}

                    Si tienes alguna pregunta, no dudes en contactarnos.

                    ¡Gracias por confiar en nosotros!
                    """

                    # Enviar el correo
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,  # Remitente configurado en settings.py
                        [recipient_email],           # Receptor
                        fail_silently=False,         # Si hay un error, no pasa desapercibido
                    )
            except Exception as e:
                print(f"Error enviando correo: {e}")

    return render(request, 'cursos/success.html', {'ultimo_pedido': ultimo_pedido})

def cancel_view(request):
    pedido_id = request.session.get('ultimo_pedido_id')
    ultimo_pedido = None
    print(pedido_id)
    if pedido_id:
        # Intentar recuperar el pedido
        ultimo_pedido = get_object_or_404(Pedido, id=pedido_id)
        ultimo_pedido.delete()
    return render(request, 'cursos/cancel.html', {'ultimo_pedido': ultimo_pedido})

