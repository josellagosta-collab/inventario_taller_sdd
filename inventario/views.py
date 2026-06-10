from django.shortcuts import render, get_object_or_404, redirect
from .models import Material, Categoria
from .forms import MaterialForm
from django.db.models import Q
from django.core.paginator import Paginator

def lista_materiales(request):
    materiales = Material.objects.all()
    categorias = Categoria.objects.all()

    busqueda = request.GET.get("busqueda", "")
    categoria_id = request.GET.get("categoria", "")
    estado = request.GET.get("estado", "")

    if busqueda:
        materiales = materiales.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo_inventario__icontains=busqueda) |
            Q(marca__icontains=busqueda) |
            Q(modelo__icontains=busqueda) |
            Q(numero_serie__icontains=busqueda)
        )

    if categoria_id:
        materiales = materiales.filter(categoria_id=categoria_id)

    if estado:
        materiales = materiales.filter(estado=estado)

    paginator = Paginator(materiales, 10)
    numero_pagina = request.GET.get("page")
    pagina_materiales = paginator.get_page(numero_pagina)

    return render(request, "inventario/lista_materiales.html", {
        "materiales": pagina_materiales,
        "categorias": categorias,
        "busqueda": busqueda,
        "categoria_id": categoria_id,
        "estado": estado,
        "estados": Material.ESTADOS,
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
    
def editar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = MaterialForm(request.POST, instance=material)

        if form.is_valid():
            material = form.save()
            return redirect("inventario:detalle_material", material_id=material.id)

    else:
        form = MaterialForm(instance=material)

    return render(request, "inventario/editar_material.html", {
        "form": form,
        "material": material
    })
    
def retirar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        material.estado = "retirado"
        material.save()
        return redirect("inventario:lista_materiales")

    return render(request, "inventario/retirar_material.html", {
        "material": material
    })