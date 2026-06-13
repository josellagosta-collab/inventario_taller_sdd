from django.db import models
from django.contrib.auth.models import User
from inventario.models import Material


class Incidencia(models.Model):
    PRIORIDADES = [
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
        ("critica", "Crítica"),
    ]

    ESTADOS = [
        ("abierta", "Abierta"),
        ("en_revision", "En revisión"),
        ("en_reparacion", "En reparación"),
        ("resuelta", "Resuelta"),
        ("cerrada", "Cerrada"),
    ]

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name="incidencias"
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="incidencias_creadas"
    )

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    prioridad = models.CharField(
        max_length=20,
        choices=PRIORIDADES,
        default="media"
    )

    estado = models.CharField(
        max_length=30,
        choices=ESTADOS,
        default="abierta"
    )

    solucion = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Incidencia"
        verbose_name_plural = "Incidencias"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.titulo} - {self.material.nombre}"


class ComentarioIncidencia(models.Model):
    incidencia = models.ForeignKey(
        Incidencia,
        on_delete=models.CASCADE,
        related_name="comentarios"
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Comentario de incidencia"
        verbose_name_plural = "Comentarios de incidencias"
        ordering = ["fecha"]

    def __str__(self):
        return f"Comentario en {self.incidencia.titulo}"