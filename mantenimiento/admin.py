from django.contrib import admin

from .models import Mantenimiento


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
