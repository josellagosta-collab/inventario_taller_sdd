from django.shortcuts import render, get_object_or_404, redirect
from .models import Material
from .forms import MaterialForm


def lista_materiales(request):
    materiales = Material.objects.all()
    return render(request, "inventario/lista_materiales.html", {
        "materiales": materiales
    })


def detalle_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, "inventario/detalle_material.html", {
        "material": material
    })


def crear_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)

        if form.is_valid():
            material = form.save()
            return redirect("inventario:detalle_material", material_id=material.id)

    else:
        form = MaterialForm()

    return render(request, "inventario/crear_material.html", {
        "form": form
    })