import logging

from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.dispatch import receiver

from .models import RegistroAuditoria
from .services import obtener_ip, registrar_accion


security_logger = logging.getLogger("seguridad")


@receiver(user_logged_in)
def auditar_inicio_sesion(sender, request, user, **kwargs):
    registrar_accion(
        request,
        "iniciar_sesion",
        f"Inicio de sesión correcto para el usuario {user.username}",
        user
    )
    security_logger.info(
        "Inicio de sesión correcto usuario=%s ip=%s",
        user.username,
        obtener_ip(request),
    )


@receiver(user_logged_out)
def auditar_cierre_sesion(sender, request, user, **kwargs):
    if user is not None:
        registrar_accion(
            request,
            "cerrar_sesion",
            f"Cierre de sesión del usuario {user.username}",
            user
        )
        security_logger.info(
            "Cierre de sesión usuario=%s ip=%s",
            user.username,
            obtener_ip(request),
        )
        return

    RegistroAuditoria.objects.create(
        accion="cerrar_sesion",
        descripcion="Cierre de sesión sin usuario asociado",
        ip=obtener_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:255] if request else "",
    )
    security_logger.info(
        "Cierre de sesión sin usuario asociado ip=%s",
        obtener_ip(request),
    )


@receiver(user_login_failed)
def auditar_login_fallido(sender, credentials, request, **kwargs):
    username = credentials.get("username", "")

    RegistroAuditoria.objects.create(
        accion="login_fallido",
        descripcion=f"Intento fallido de inicio de sesión para el usuario {username}",
        ip=obtener_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:255] if request else "",
    )
    security_logger.warning(
        "Intento fallido de inicio de sesión usuario=%s ip=%s",
        username,
        obtener_ip(request),
    )
