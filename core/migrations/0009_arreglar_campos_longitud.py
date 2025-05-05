from django.db import migrations, models

def limpiar_datos(apps, schema_editor):
    """Limpia datos en campos de contraseña y sesión para preparar migración"""
    Egresado = apps.get_model('core', 'Egresado')
    Administrador = apps.get_model('core', 'Administrador')
    
    # Establecer valores vacíos para evitar problemas de longitud
    Egresado.objects.all().update(contraseña='', sesion=None)
    Administrador.objects.all().update(sesion=None)

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0005_alter_egresado_contraseña'),  # Reemplaza con la última migración exitosa
    ]

    operations = [
        # Ejecuta la función de limpieza
        migrations.RunPython(limpiar_datos),
        
        # Altera los campos para aumentar tamaño
        migrations.AlterField(
            model_name='egresado',
            name='contraseña',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='egresado',
            name='sesion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='administrador',
            name='contraseña',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='administrador',
            name='sesion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]