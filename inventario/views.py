from django.shortcuts import render
from .models import Material


def lista_materiales(request):
    materiales = Material.objects.all()
    return render(request, "inventario/lista_materiales.html", {
        "materiales": materiales
    })
