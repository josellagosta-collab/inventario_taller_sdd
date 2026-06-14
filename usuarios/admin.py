from django.contrib import admin

from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "tipo_usuario",
        "departamento",
        "telefono",
        "puede_recibir_prestamos",
    ]
    list_filter = [
        "tipo_usuario",
        "puede_recibir_prestamos",
    ]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "departamento",
        "telefono",
    ]
