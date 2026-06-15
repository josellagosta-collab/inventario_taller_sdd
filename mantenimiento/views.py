from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from auditoria.services import registrar_accion
from inventario.models import Material, MovimientoInventario
from usuarios.decorators import pertenece_a_grupo

from .forms import MantenimientoForm


@login_required
@pertenece_a_grupo("Administradores")
def crear_mantenimiento_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = MantenimientoForm(request.POST)

        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.material = material

            if request.user.is_authenticated:
                mantenimiento.tecnico = request.user

            mantenimiento.save()

            descripcion = (
                f"Mantenimiento registrado. "
                f"Tipo: {mantenimiento.get_tipo_display()}. "
                f"Resultado: {mantenimiento.get_resultado_display()}."
            )
            MovimientoInventario.objects.create(
                material=material,
                tipo="ajuste",
                usuario=request.user if request.user.is_authenticated else None,
                descripcion=descripcion,
            )
            registrar_accion(
                request,
                "crear",
                descripcion,
                mantenimiento,
            )
            return redirect("inventario:detalle_material", material_id=material.id)
    else:
        form = MantenimientoForm()

    return render(request, "mantenimiento/form_mantenimiento.html", {
        "form": form,
        "material": material,
    })
