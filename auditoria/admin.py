from django.contrib import admin

from .models import RegistroAuditoria


@admin.register(RegistroAuditoria)
class RegistroAuditoriaAdmin(admin.ModelAdmin):
    list_display = (
        "fecha",
        "usuario",
        "accion",
        "content_type",
        "object_id",
        "ip",
    )
    list_filter = ("accion", "content_type", "fecha")
    search_fields = (
        "usuario__username",
        "descripcion",
        "objeto_repr",
        "object_id",
        "ip",
    )
    readonly_fields = (
        "usuario",
        "accion",
        "descripcion",
        "content_type",
        "object_id",
        "objeto_repr",
        "ip",
        "user_agent",
        "fecha",
    )
    ordering = ("-fecha",)
