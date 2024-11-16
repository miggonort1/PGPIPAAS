from django.contrib import admin
from .models import *

admin.site.register(Curso)
admin.site.register(Usuario)
admin.site.register(Carrito)
admin.site.register(Pedido)
admin.site.register(CarritoCurso)