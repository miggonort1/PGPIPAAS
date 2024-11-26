# views.py
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm
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


def home(request):
    # Obtener todos los cursos
    cursos = Curso.objects.all()

    # Filtros de cursos
    hoy = date.today()
    cursos_pronto = cursos.filter(fecha_inicio__gte=hoy).order_by('fecha_inicio')
    cursos_pocas_plazas = cursos.filter(plazas_disponibles__lt=20).order_by('plazas_disponibles')
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
        return redirect('inicioSesion')  # Redirige a la página de inicio de sesión (ajusta la URL según corresponda)
    

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

        # Obtener el carrito desde la sesión
        carrito = request.session.get('carrito', {})

        # Si el carrito no existe, crear uno vacío
        if not carrito:
            carrito = {}

        # Obtener el curso y añadirlo al carrito
        try:
            curso = Curso.objects.get(id=curso_id)
            
            # Si el curso ya está en el carrito, incrementar la cantidad
            if curso_id in carrito:
                carrito[curso_id]['cantidad'] += 1
            else:
                # Si el curso no está en el carrito, agregarlo con cantidad 1
                carrito[curso_id] = {
                    'nombre': curso.nombre,
                    'precio': str(curso.precio),  # Convertir el precio a string por seguridad en JSON
                    'cantidad': 1
                }

            # Guardar el carrito en la sesión
            request.session['carrito'] = carrito

            return JsonResponse({'success': True, 'message': 'Curso añadido al carrito.'})
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
            nombre_comprador = data.get("nombre_comprador")
            email_comprador = data.get("email_comprador")
            direccion_envio = data.get("direccion_envio")
            ciudad_envio = data.get("ciudad_envio")
            provincia_envio = data.get("provincia_envio")
            codigo_postal_envio = data.get("codigo_postal_envio")
            payment_method = data.get("payment-method")

            
            # Calcula el total (sumar precios de cursos)
            total = 0
            cursos = []
            for i in range(len(data)):  # Iteramos sobre los índices de los cursos
                if f"course_id-{i}-0" in data:
                    course_id = int(data[f"course_id-{i}-0"])
                    course_quantity = int(data[f"course_quantity-{i}-0"])
                    
                    email = data.get(f"email-{i}-0")  # email para este curso
                    nombre = data.get(f"name-{i}-0") 
                    course = Curso.objects.get(id=course_id)
                    total += course.precio * course_quantity  # Calculamos el total

                    cursos.append({
                        'course': course,
                        'quantity': course_quantity,
                        'precio_unitario': course.precio,
                        'nombre': nombre,
                        'email': email,
                    })
            codigo_seguimiento = str(uuid.uuid4())
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
            items = data.get("items", [])
            line_items = []
            for item in items:
                curso_id = item.get("curso_id")
                cantidad = item.get("cantidad",1)
            
                curso = Curso.objects.get(id=curso_id)
            
                line_items.append({
                    'price': curso.price_id,
                    'quantity': cantidad,
                })
                print(item)

            checkout_session = stripe.checkout.Session.create(
                line_items= line_items,
                mode='payment',
                success_url=YOUR_DOMAIN + '/success.html',
                cancel_url=YOUR_DOMAIN + '/cancel.html',
            )
            return JsonResponse({'url': checkout_session.url})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


def success_view(request):
    return render(request, 'cursos/success.html')

def cancel_view(request):
    return render(request, 'cursos/cancel.html')