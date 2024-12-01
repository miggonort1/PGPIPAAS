from django.core.exceptions import ValidationError
import re

def validate_phone_number(value):
    phone_regex = re.compile(r'^\+?1?\d{9,15}$')  # Formato internacional
    if not phone_regex.match(value):
        raise ValidationError("El número de teléfono no es válido. Debe tener entre 9 y 15 dígitos y puede incluir un prefijo internacional.")
