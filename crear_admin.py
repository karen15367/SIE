from django.contrib.auth.hashers import make_password
from core.models import Administrador

# Crea el primer administrador
admin = Administrador(
    rfc="XAXX010101000",
    nombre="Administrador Principal",
    correo="admin@example.com",
    contraseña=make_password("admin1234"),
    carrera="general",
)
admin.save()

print(f"Administrador {admin.nombre} creado exitosamente con RFC: {admin.rfc}")