# cursos/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.admin.models import LogEntry
from cursos.models import Usuario  # Asegúrate de que esta línea esté presente

@receiver(post_delete, sender=Usuario)
def eliminar_logs_usuario(sender, instance, **kwargs):
    # Elimina los registros de log asociados con el usuario en auth_user
    LogEntry.objects.filter(user=instance).delete()
