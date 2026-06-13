from django.contrib import admin
from .models import Incidencia, ComentarioIncidencia


class ComentarioIncidenciaInline(admin.TabularInline):
    model = ComentarioIncidencia
    extra = 1


@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "material",
        "usuario",
        "prioridad",
        "estado",
        "fecha_creacion",
        "fecha_cierre",
    )

    list_filter = (
        "prioridad",
        "estado",
        "fecha_creacion",
    )

    search_fields = (
        "titulo",
        "descripcion",
        "material__nombre",
        "material__codigo_inventario",
    )

    inlines = [ComentarioIncidenciaInline]


@admin.register(ComentarioIncidencia)
class ComentarioIncidenciaAdmin(admin.ModelAdmin):
    list_display = (
        "incidencia",
        "usuario",
        "fecha",
    )

    search_fields = (
        "comentario",
        "incidencia__titulo",
    )
    from django.contrib import admin

# Register your models here.
