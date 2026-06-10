from django.shortcuts import render, get_object_or_404
from .models import Material


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