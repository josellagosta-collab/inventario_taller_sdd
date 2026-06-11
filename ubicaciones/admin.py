from django.contrib import admin
from .models import Edificio, Aula, Armario, Estanteria, Caja, Ubicacion


@admin.register(Edificio)
class EdificioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "edificio", "descripcion")
    list_filter = ("edificio",)
    search_fields = ("nombre", "edificio__nombre")


@admin.register(Armario)
class ArmarioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "aula", "descripcion")
    list_filter = ("aula",)
    search_fields = ("nombre", "aula__nombre")


@admin.register(Estanteria)
class EstanteriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "armario", "descripcion")
    list_filter = ("armario",)
    search_fields = ("nombre", "armario__nombre")


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "estanteria", "descripcion")
    list_filter = ("estanteria",)
    search_fields = ("nombre", "estanteria__nombre")


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = (
        "edificio",
        "aula",
        "armario",
        "estanteria",
        "caja",
        "posicion",
    )
    list_filter = ("edificio", "aula", "armario", "estanteria", "caja")
    search_fields = (
        "edificio__nombre",
        "aula__nombre",
        "armario__nombre",
        "estanteria__nombre",
        "caja__nombre",
        "posicion",
    )