from django.db import models
from ubicaciones.models import Ubicacion


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