from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


class RegistroAuditoria(models.Model):
    ACCIONES = [
        ("crear", "Crear"),
        ("editar", "Editar"),
        ("eliminar", "Eliminar"),
        ("retirar", "Retirar"),
        ("prestar", "Prestar"),
        ("devolver", "Devolver"),
        ("reservar", "Reservar"),
        ("cancelar_reserva", "Cancelar reserva"),
        ("convertir_reserva", "Convertir reserva"),
        ("exportar", "Exportar"),
        ("acceder", "Acceder"),
        ("otro", "Otro"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="registros_auditoria"
    )

    accion = models.CharField(
        max_length=50,
        choices=ACCIONES,
        default="otro"
    )

    descripcion = models.TextField()

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    object_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    objeto_repr = models.CharField(
        max_length=255,
        blank=True
    )

    ip = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    user_agent = models.CharField(
        max_length=255,
        blank=True
    )

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de auditoría"
        verbose_name_plural = "Registros de auditoría"
        ordering = ["-fecha"]

    def __str__(self):
        usuario = self.usuario.username if self.usuario else "Sistema"
        return f"{self.fecha:%d/%m/%Y %H:%M} - {usuario} - {self.get_accion_display()}"
