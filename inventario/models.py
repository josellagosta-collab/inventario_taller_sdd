from django.db import models
from ubicaciones.models import Ubicacion
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Subcategoria(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name="subcategorias"
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Subcategoría"
        verbose_name_plural = "Subcategorías"
        ordering = ["categoria__nombre", "nombre"]
        unique_together = ("categoria", "nombre")

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    web = models.URLField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Material(models.Model):
    ESTADOS = [
        ("disponible", "Disponible"),
        ("prestado", "Prestado"),
        ("reservado", "Reservado"),
        ("averiado", "Averiado"),
        ("en_reparacion", "En reparación"),
        ("fuera_servicio", "Fuera de servicio"),
        ("retirado", "Retirado"),
        ("perdido", "Perdido"),
    ]

    codigo_inventario = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="materiales"
    )

    subcategoria = models.ForeignKey(
        Subcategoria,
        on_delete=models.PROTECT,
        related_name="materiales",
        blank=True,
        null=True
    )

    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        related_name="materiales",
        blank=True,
        null=True
    )

    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    numero_serie = models.CharField(max_length=200, blank=True, null=True)

    cantidad = models.PositiveIntegerField(default=1)
    stock_minimo = models.PositiveIntegerField(default=0)

    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    fecha_compra = models.DateField(blank=True, null=True)
    garantia_hasta = models.DateField(blank=True, null=True)

    estado = models.CharField(
        max_length=50,
        choices=ESTADOS,
        default="disponible"
    )

    ubicacion = models.ForeignKey(
    Ubicacion,
    on_delete=models.SET_NULL,
    related_name="materiales",
    blank=True,
    null=True
    )

    observaciones = models.TextField(blank=True, null=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiales"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo_inventario} - {self.nombre}"

    def clean(self):
        errores = {}
        hoy = timezone.now().date()

        if self.codigo_inventario:
            self.codigo_inventario = self.codigo_inventario.strip()

        if self.nombre:
            self.nombre = self.nombre.strip()

        if self.numero_serie:
            self.numero_serie = self.numero_serie.strip()

        if self.precio_compra is not None and self.precio_compra < 0:
            errores["precio_compra"] = "El precio de compra no puede ser negativo."

        if self.fecha_compra and self.fecha_compra > hoy:
            errores["fecha_compra"] = "La fecha de compra no puede ser futura."

        if self.fecha_compra and self.garantia_hasta and self.garantia_hasta < self.fecha_compra:
            errores["garantia_hasta"] = (
                "La fecha de garantía no puede ser anterior a la fecha de compra."
            )

        if self.subcategoria and self.categoria_id and self.subcategoria.categoria_id != self.categoria_id:
            errores["subcategoria"] = (
                "La subcategoría seleccionada no pertenece a la categoría indicada."
            )

        if self.cantidad == 0 and self.estado in ["disponible", "reservado", "prestado"]:
            errores["cantidad"] = (
                "La cantidad debe ser mayor que cero para materiales disponibles, reservados o prestados."
            )

        if errores:
            raise ValidationError(errores)
    
from django.contrib.auth.models import User


class MovimientoInventario(models.Model):
    TIPOS_MOVIMIENTO = [
        ("alta", "Alta"),
        ("edicion", "Edición"),
        ("retirada", "Retirada"),
        ("prestamo", "Préstamo"),
        ("devolucion", "Devolución"),
        ("traslado", "Traslado"),
        ("ajuste", "Ajuste"),
    ]

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="movimientos"
    )

    tipo = models.CharField(
        max_length=50,
        choices=TIPOS_MOVIMIENTO
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    descripcion = models.TextField(blank=True, null=True)

    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Movimiento de inventario"
        verbose_name_plural = "Movimientos de inventario"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.material.nombre} - {self.get_tipo_display()}"
