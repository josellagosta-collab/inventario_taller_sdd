from django.contrib import admin
from .models import Documento, Fotografia


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "material",
        "tipo_documento",
        "usuario",
        "fecha_subida",
    )

    list_filter = (
        "tipo_documento",
        "fecha_subida",
    )

    search_fields = (
        "nombre",
        "material__nombre",
        "material__codigo_inventario",
    )


@admin.register(Fotografia)
class FotografiaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "material",
        "usuario",
        "fecha_subida",
    )

    list_filter = (
        "fecha_subida",
    )

    search_fields = (
        "titulo",
        "material__nombre",
        "material__codigo_inventario",
    )
