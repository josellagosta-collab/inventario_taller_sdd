from django.db import models
from django.contrib.auth.models import User
from inventario.models import Material


class Prestamo(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("devuelto", "Devuelto"),
        ("retrasado", "Retrasado"),
        ("perdido", "Perdido"),
    ]

    usuario_receptor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="prestamos_recibidos"
    )

    profesor_responsable = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="prestamos_gestionados"
    )

    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_prevista_devolucion = models.DateField()
    fecha_devolucion_real = models.DateField(blank=True, null=True)

    estado = models.CharField(
        max_length=50,
        choices=ESTADOS,
        default="activo"
    )

    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ["-fecha_prestamo"]

    def __str__(self):
        return f"Préstamo {self.id} - {self.usuario_receptor.username}"


class LineaPrestamo(models.Model):
    prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        related_name="lineas"
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name="lineas_prestamo"
    )

    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Línea de préstamo"
        verbose_name_plural = "Líneas de préstamo"

    def __str__(self):
        return f"{self.material.nombre} x {self.cantidad}"
