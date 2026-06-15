from django.contrib import admin

from .models import Mantenimiento, PlanMantenimiento


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = [
        "material",
        "tipo",
        "fecha",
        "resultado",
        "tecnico",
        "coste",
        "proxima_revision",
    ]
    list_filter = [
        "tipo",
        "resultado",
        "fecha",
        "proxima_revision",
    ]
    search_fields = [
        "material__nombre",
        "material__codigo_inventario",
        "tecnico__username",
        "descripcion",
    ]
    autocomplete_fields = [
        "material",
        "tecnico",
    ]


@admin.register(PlanMantenimiento)
class PlanMantenimientoAdmin(admin.ModelAdmin):
    list_display = [
        "nombre",
        "material",
        "tipo",
        "frecuencia_dias",
        "proxima_revision",
        "responsable",
        "activo",
    ]
    list_filter = [
        "tipo",
        "activo",
        "proxima_revision",
    ]
    search_fields = [
        "nombre",
        "material__nombre",
        "material__codigo_inventario",
        "responsable__username",
        "descripcion",
    ]
    autocomplete_fields = [
        "material",
        "responsable",
    ]
