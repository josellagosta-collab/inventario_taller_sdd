from datetime import timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

from inventario.models import Material


class Mantenimiento(models.Model):
    TIPO_PREVENTIVO = "preventivo"
    TIPO_CORRECTIVO = "correctivo"
    TIPO_PREDICTIVO = "predictivo"

    TIPOS = [
        (TIPO_PREVENTIVO, "Preventivo"),
        (TIPO_CORRECTIVO, "Correctivo"),
        (TIPO_PREDICTIVO, "Predictivo"),
    ]

    RESULTADO_OK = "ok"
    RESULTADO_REPARADO = "reparado"
    RESULTADO_PENDIENTE = "pendiente"
    RESULTADO_NO_REPARABLE = "no_reparable"

    RESULTADOS = [
        (RESULTADO_OK, "Correcto"),
        (RESULTADO_REPARADO, "Reparado"),
        (RESULTADO_PENDIENTE, "Pendiente"),
        (RESULTADO_NO_REPARABLE, "No reparable"),
    ]

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name="mantenimientos",
        verbose_name="material",
    )
    tecnico = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="mantenimientos_realizados",
        verbose_name="técnico responsable",
    )
    tipo = models.CharField(
        "tipo",
        max_length=20,
        choices=TIPOS,
        default=TIPO_PREVENTIVO,
    )
    fecha = models.DateField(
        "fecha",
        default=timezone.now,
    )
    descripcion = models.TextField(
        "descripción",
    )
    resultado = models.CharField(
        "resultado",
        max_length=20,
        choices=RESULTADOS,
        default=RESULTADO_OK,
    )
    coste = models.DecimalField(
        "coste",
        max_digits=10,
        decimal_places=2,
        default=0,
    )
    proxima_revision = models.DateField(
        "próxima revisión",
        blank=True,
        null=True,
    )
    observaciones = models.TextField(
        "observaciones",
        blank=True,
    )
    creado_en = models.DateTimeField(
        "creado en",
        auto_now_add=True,
    )
    actualizado_en = models.DateTimeField(
        "actualizado en",
        auto_now=True,
    )

    class Meta:
        verbose_name = "mantenimiento"
        verbose_name_plural = "mantenimientos"
        ordering = ["-fecha", "-creado_en"]

    def clean(self):
        errores = {}

        if self.coste is not None and self.coste < 0:
            errores["coste"] = "El coste no puede ser negativo."

        if self.fecha and self.fecha > timezone.now().date():
            errores["fecha"] = "La fecha del mantenimiento no puede ser futura."

        if self.fecha and self.proxima_revision and self.proxima_revision < self.fecha:
            errores["proxima_revision"] = (
                "La próxima revisión no puede ser anterior al mantenimiento."
            )

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"{self.material} - {self.get_tipo_display()} - {self.fecha}"


class PlanMantenimiento(models.Model):
    DIAS_ALERTA_REVISION = 7

    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name="planes_mantenimiento",
        verbose_name="material",
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="planes_mantenimiento",
        verbose_name="responsable",
    )
    nombre = models.CharField(
        "nombre",
        max_length=150,
    )
    tipo = models.CharField(
        "tipo",
        max_length=20,
        choices=Mantenimiento.TIPOS,
        default=Mantenimiento.TIPO_PREVENTIVO,
    )
    descripcion = models.TextField(
        "descripción",
        blank=True,
    )
    frecuencia_dias = models.PositiveIntegerField(
        "frecuencia en días",
        default=30,
    )
    fecha_inicio = models.DateField(
        "fecha de inicio",
        default=timezone.now,
    )
    proxima_revision = models.DateField(
        "próxima revisión",
    )
    activo = models.BooleanField(
        "activo",
        default=True,
    )
    observaciones = models.TextField(
        "observaciones",
        blank=True,
    )
    creado_en = models.DateTimeField(
        "creado en",
        auto_now_add=True,
    )
    actualizado_en = models.DateTimeField(
        "actualizado en",
        auto_now=True,
    )

    class Meta:
        verbose_name = "plan de mantenimiento"
        verbose_name_plural = "planes de mantenimiento"
        ordering = ["proxima_revision", "material__nombre"]

    def clean(self):
        errores = {}

        if self.frecuencia_dias is not None and self.frecuencia_dias <= 0:
            errores["frecuencia_dias"] = (
                "La frecuencia debe ser mayor que cero días."
            )

        if (
            self.fecha_inicio
            and self.proxima_revision
            and self.proxima_revision < self.fecha_inicio
        ):
            errores["proxima_revision"] = (
                "La próxima revisión no puede ser anterior a la fecha de inicio."
            )

        if errores:
            raise ValidationError(errores)

    def __str__(self):
        return f"{self.nombre} - {self.material}"

    @property
    def dias_hasta_revision(self):
        return (self.proxima_revision - timezone.now().date()).days

    @property
    def dias_revision_absolutos(self):
        return abs(self.dias_hasta_revision)

    @property
    def estado_revision(self):
        if not self.activo:
            return "inactivo"

        hoy = timezone.now().date()
        fecha_limite_alerta = hoy + timedelta(days=self.DIAS_ALERTA_REVISION)

        if self.proxima_revision < hoy:
            return "vencido"

        if self.proxima_revision <= fecha_limite_alerta:
            return "proximo"

        return "al_dia"

    @property
    def estado_revision_display(self):
        etiquetas = {
            "inactivo": "Inactivo",
            "vencido": "Revisión vencida",
            "proximo": "Próxima revisión",
            "al_dia": "Al día",
        }
        return etiquetas[self.estado_revision]
