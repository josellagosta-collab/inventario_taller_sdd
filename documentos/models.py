from django.db import models
from django.contrib.auth.models import User
from inventario.models import Material


class Documento(models.Model):

    TIPOS_DOCUMENTO = [
        ("manual", "Manual"),
        ("factura", "Factura"),
        ("garantia", "Garantía"),
        ("esquema", "Esquema"),
        ("fotografia", "Fotografía"),
        ("proyecto", "Proyecto"),
        ("configuracion", "Configuración"),
        ("otro", "Otro"),
    ]

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="documentos"
    )

    nombre = models.CharField(max_length=200)

    descripcion = models.TextField(blank=True, null=True)

    archivo = models.FileField(
        upload_to="documentos_material/"
    )

    tipo_documento = models.CharField(
        max_length=50,
        choices=TIPOS_DOCUMENTO,
        default="otro"
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-fecha_subida"]

    def __str__(self):
        return f"{self.nombre} - {self.material.nombre}"


class Fotografia(models.Model):
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="fotografias"
    )

    titulo = models.CharField(max_length=200)

    imagen = models.ImageField(
        upload_to="fotografias_material/"
    )

    descripcion = models.TextField(blank=True, null=True)

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fotografía"
        verbose_name_plural = "Fotografías"
        ordering = ["-fecha_subida"]

    def __str__(self):
        return f"{self.titulo} - {self.material.nombre}"
