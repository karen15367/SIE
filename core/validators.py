from django.core.validators import RegexValidator

# Solo letras y espacios
solo_letras_espacios = RegexValidator(
    regex=r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$',
    message='Este campo solo puede contener letras y espacios.'
)

# CURP (18 caracteres)
curp_validator = RegexValidator(
    regex=r'^[A-Z]{4}\d{6}[A-Z]{6}\d{2}$',
    message='El CURP debe tener el formato correcto (18 caracteres).'
)

# RFC (13 caracteres)
rfc_validator = RegexValidator(
    regex=r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$',
    message='El RFC debe tener el formato correcto (13 caracteres).'
)

# Número de control (9 caracteres)
numero_control_validator = RegexValidator(
    regex=r'^\d{9}$',
    message='El número de control debe contener exactamente 9 dígitos.'
)

# Teléfono mexicano estándar
telefono_validator = RegexValidator(
    regex=r'^\d{10}$',
    message='El número de teléfono debe contener exactamente 10 dígitos.'
)
