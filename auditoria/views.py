from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from usuarios.decorators import pertenece_a_grupo

from .models import RegistroAuditoria


@login_required
@pertenece_a_grupo("Administradores")
def lista_auditoria(request):
    registros = RegistroAuditoria.objects.select_related(
        "usuario",
        "content_type"
    ).all()

    busqueda = request.GET.get("busqueda", "")
    accion = request.GET.get("accion", "")

    if busqueda:
        registros = registros.filter(
            Q(usuario__username__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(objeto_repr__icontains=busqueda) |
            Q(object_id__icontains=busqueda) |
            Q(ip__icontains=busqueda)
        )

    if accion:
        registros = registros.filter(accion=accion)

    paginator = Paginator(registros, 20)
    numero_pagina = request.GET.get("page")
    pagina_registros = paginator.get_page(numero_pagina)

    return render(request, "auditoria/lista_auditoria.html", {
        "registros": pagina_registros,
        "busqueda": busqueda,
        "accion": accion,
        "acciones": RegistroAuditoria.ACCIONES,
    })
