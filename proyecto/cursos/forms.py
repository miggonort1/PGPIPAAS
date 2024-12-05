from django import forms
from .models import Usuario, Curso, Pedido

class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = Usuario
        fields = ['email', 'nombre_usuario', 'nombre', 'apellido', 'direccion_entrega', 
                  'ciudad', 'provincia', 'codigo_postal', 'telefono']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Verificar que las contraseñas coincidan
        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'direccion_entrega', 'ciudad', 'provincia', 'codigo_postal', 'telefono','payment']

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nombre', 'descripcion', 'fecha_inicio', 'duracion_semanas', 'plazas_disponibles', 'precio']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario', 'email', 'nombre', 'estado', 'direccion_envio', 'ciudad_envio','provincia_envio', 'codigo_postal_envio', 'total']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'direccion_envio': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad_envio': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia_envio': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal_envio': forms.TextInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
