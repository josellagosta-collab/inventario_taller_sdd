from django.contrib import admin
from .models import Prestamo, LineaPrestamo, Reserva


class LineaPrestamoInline(admin.TabularInline):
    model = LineaPrestamo
    extra = 1


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario_receptor",
        "profesor_responsable",
        "fecha_prestamo",
        "fecha_prevista_devolucion",
        "fecha_devolucion_real",
        "estado",
    )

    list_filter = (
        "estado",
        "fecha_prestamo",
        "fecha_prevista_devolucion",
    )

    search_fields = (
        "usuario_receptor__username",
        "profesor_responsable__username",
        "observaciones",
    )

    inlines = [LineaPrestamoInline]


@admin.register(LineaPrestamo)
class LineaPrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "prestamo",
        "material",
        "cantidad",
    )

    search_fields = (
        "material__nombre",
        "material__codigo_inventario",
    )
    
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario_reserva",
        "profesor_responsable",
        "material",
        "cantidad",
        "fecha_reserva",
        "fecha_prevista_recogida",
        "estado",
    )

    list_filter = (
        "estado",
        "fecha_reserva",
        "fecha_prevista_recogida",
    )

    search_fields = (
        "usuario_reserva__username",
        "profesor_responsable__username",
        "material__nombre",
        "material__codigo_inventario",
        "observaciones",
    )