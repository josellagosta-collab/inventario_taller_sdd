from django.contrib import admin
from .models import Categoria, Subcategoria, Proveedor, Material


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(Subcategoria)
class SubcategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria")
    list_filter = ("categoria",)
    search_fields = ("nombre", "categoria__nombre")


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "email", "web")
    search_fields = ("nombre", "email")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        "codigo_inventario",
        "nombre",
        "categoria",
        "subcategoria",
        "marca",
        "modelo",
        "cantidad",
        "estado",
    )
    list_filter = ("estado", "categoria", "subcategoria", "marca")
    search_fields = (
        "codigo_inventario",
        "nombre",
        "marca",
        "modelo",
        "numero_serie",
    )