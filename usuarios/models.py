from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    TIPO_ADMINISTRADOR = "administrador"
    TIPO_PROFESOR = "profesor"
    TIPO_TECNICO = "tecnico"
    TIPO_ALUMNO = "alumno"

    TIPOS_USUARIO = [
        (TIPO_ADMINISTRADOR, "Administrador"),
        (TIPO_PROFESOR, "Profesor"),
        (TIPO_TECNICO, "Técnico"),
        (TIPO_ALUMNO, "Alumno"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name="usuario",
    )
    tipo_usuario = models.CharField(
        "tipo de usuario",
        max_length=20,
        choices=TIPOS_USUARIO,
        default=TIPO_PROFESOR,
    )
    departamento = models.CharField(
        "departamento",
        max_length=120,
        blank=True,
    )
    telefono = models.CharField(
        "teléfono",
        max_length=30,
        blank=True,
    )
    puede_recibir_prestamos = models.BooleanField(
        "puede recibir préstamos",
        default=True,
    )
    observaciones = models.TextField(
        "observaciones",
        blank=True,
    )
    creado_en = models.DateTimeField(
        "creado en",
        auto_now_add=True,
    )
    actualizado_en = models.DateTimeField(
        "actualizado en",
        auto_now=True,
    )

    class Meta:
        verbose_name = "perfil de usuario"
        verbose_name_plural = "perfiles de usuario"

    def __str__(self):
        return f"Perfil de {self.user.username}"
