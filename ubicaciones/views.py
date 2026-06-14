from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import ProtectedError, Q
from django.shortcuts import get_object_or_404, redirect, render

from auditoria.services import registrar_accion
from usuarios.decorators import pertenece_a_grupo

from .forms import UbicacionForm
from .models import Edificio, Ubicacion


@login_required
def lista_ubicaciones(request):
    ubicaciones = Ubicacion.objects.select_related(
        "edificio",
        "aula",
        "armario",
        "estanteria",
        "caja",
    ).all()

    edificios = Edificio.objects.all()

    busqueda = request.GET.get("busqueda", "")
    edificio_id = request.GET.get("edificio", "")

    if busqueda:
        ubicaciones = ubicaciones.filter(
            Q(edificio__nombre__icontains=busqueda) |
            Q(aula__nombre__icontains=busqueda) |
            Q(armario__nombre__icontains=busqueda) |
            Q(estanteria__nombre__icontains=busqueda) |
            Q(caja__nombre__icontains=busqueda) |
            Q(posicion__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    if edificio_id:
        ubicaciones = ubicaciones.filter(edificio_id=edificio_id)

    paginator = Paginator(ubicaciones, 10)
    numero_pagina = request.GET.get("page")
    pagina_ubicaciones = paginator.get_page(numero_pagina)

    return render(request, "ubicaciones/lista_ubicaciones.html", {
        "ubicaciones": pagina_ubicaciones,
        "edificios": edificios,
        "busqueda": busqueda,
        "edificio_id": edificio_id,
    })


@login_required
@pertenece_a_grupo("Administradores")
def crear_ubicacion(request):
    if request.method == "POST":
        form = UbicacionForm(request.POST)

        if form.is_valid():
            ubicacion = form.save()
            registrar_accion(
                request,
                "crear",
                "Creación de ubicación desde la web",
                ubicacion
            )
            messages.success(request, "Ubicación creada correctamente.")
            return redirect("ubicaciones:lista_ubicaciones")

    else:
        form = UbicacionForm()

    return render(request, "ubicaciones/form_ubicacion.html", {
        "form": form,
        "titulo": "Nueva ubicación",
        "texto_boton": "Guardar ubicación",
    })


@login_required
@pertenece_a_grupo("Administradores")
def editar_ubicacion(request, ubicacion_id):
    ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)

    if request.method == "POST":
        form = UbicacionForm(request.POST, instance=ubicacion)

        if form.is_valid():
            ubicacion = form.save()
            registrar_accion(
                request,
                "editar",
                "Edición de ubicación desde la web",
                ubicacion
            )
            messages.success(request, "Ubicación actualizada correctamente.")
            return redirect("ubicaciones:lista_ubicaciones")

    else:
        form = UbicacionForm(instance=ubicacion)

    return render(request, "ubicaciones/form_ubicacion.html", {
        "form": form,
        "titulo": "Editar ubicación",
        "texto_boton": "Guardar cambios",
        "ubicacion": ubicacion,
    })


@login_required
@pertenece_a_grupo("Administradores")
def eliminar_ubicacion(request, ubicacion_id):
    ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)

    if request.method == "POST":
        try:
            descripcion = str(ubicacion)
            ubicacion.delete()
            registrar_accion(
                request,
                "eliminar",
                f"Eliminación de ubicación: {descripcion}"
            )
            messages.success(request, "Ubicación eliminada correctamente.")
            return redirect("ubicaciones:lista_ubicaciones")
        except ProtectedError:
            messages.error(
                request,
                "No se puede eliminar esta ubicación porque está asociada a materiales."
            )

    return render(request, "ubicaciones/eliminar_ubicacion.html", {
        "ubicacion": ubicacion,
    })
