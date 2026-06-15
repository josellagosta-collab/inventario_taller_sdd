from django.contrib.contenttypes.models import ContentType

from .models import RegistroAuditoria


def obtener_ip(request):
    if not request:
        return None

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def registrar_accion(request, accion, descripcion, objeto=None):
    usuario = None

    if request and hasattr(request, "user") and request.user.is_authenticated:
        usuario = request.user
       
    content_type = None
    object_id = None
    objeto_repr = ""

    if objeto is not None:
        content_type = ContentType.objects.get_for_model(objeto)
        object_id = str(objeto.pk)
        objeto_repr = str(objeto)[:255]

    return RegistroAuditoria.objects.create(
        usuario=usuario,
        accion=accion,
        descripcion=descripcion,
        content_type=content_type,
        object_id=object_id,
        objeto_repr=objeto_repr,
        ip=obtener_ip(request),
        user_agent=(request.META.get("HTTP_USER_AGENT", "")[:255] if request else ""),
    )
