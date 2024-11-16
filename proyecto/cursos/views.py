# views.py
from .models import Curso
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroUsuarioForm
from cursos.models import Usuario

def home(request):
    # Obtener todos los cursos de la base de datos
    cursos = Curso.objects.all()  # Esto obtiene todos los cursos

    # Pasar los cursos al contexto de la plantilla
    context = {
        'cursos': cursos,
    }
    
    return render(request, 'cursos/home.html', context)

def perfil(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f'Usuario: {username}, Contraseña: {password}')  # Depuración

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is None:
            # Si 'authenticate' devuelve None, significa que las credenciales no son correctas
            try:
                # Intentamos obtener al usuario de la base de datos para dar mensajes más específicos
                usuario = Usuario.objects.get(nombre_usuario=username)
                if not usuario.is_active:
                    # Si el usuario está inactivo, agregamos un mensaje
                    messages.error(request, "Tu cuenta está inactiva. No puedes iniciar sesión.")
                else:
                    # Si el nombre de usuario existe pero la contraseña es incorrecta
                    messages.error(request, "Contraseña incorrecta.")
            except Usuario.DoesNotExist:
                # Si el usuario no existe, agregamos un mensaje
                messages.error(request, "El nombre de usuario no existe.")
        else:
            # Si la autenticación fue exitosa
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.nombre_usuario}!")
            return redirect('home')  # Redirigir al inicio después de iniciar sesión
    
    return render(request, 'cursos/perfil.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Crear el usuario con la información proporcionada
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])  # Establecer la contraseña encriptada
            usuario.save()

            messages.success(request, "¡Registro exitoso! Ahora puedes iniciar sesión.")
            return redirect('perfil')  # Redirigir a la vista de inicio de sesión o al home
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = RegistroUsuarioForm()

    return render(request, 'cursos/registro.html', {'form': form})