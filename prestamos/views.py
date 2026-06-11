from .forms import PrestamoForm, LineaPrestamoForm
from .models import Prestamo
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

def crear_prestamo(request):
    if request.method == "POST":
        prestamo_form = PrestamoForm(request.POST)
        linea_form = LineaPrestamoForm(request.POST)

        if prestamo_form.is_valid() and linea_form.is_valid():
            prestamo = prestamo_form.save()

            linea = linea_form.save(commit=False)
            linea.prestamo = prestamo
            linea.save()

            material = linea.material
            material.estado = "prestado"
            material.save()

            return redirect("prestamos:lista_prestamos")

    else:
        prestamo_form = PrestamoForm()
        linea_form = LineaPrestamoForm()

    return render(request, "prestamos/crear_prestamo.html", {
        "prestamo_form": prestamo_form,
        "linea_form": linea_form,
    })
    
def lista_prestamos(request):
    prestamos = Prestamo.objects.select_related(
        "usuario_receptor",
        "profesor_responsable"
    ).prefetch_related("lineas__material")

    return render(request, "prestamos/lista_prestamos.html", {
        "prestamos": prestamos,
    })
    
def devolver_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if request.method == "POST":
        prestamo.estado = "devuelto"
        prestamo.fecha_devolucion_real = timezone.now().date()
        prestamo.save()

        for linea in prestamo.lineas.all():
            material = linea.material
            material.estado = "disponible"
            material.save()

        return redirect("prestamos:lista_prestamos")

    return render(request, "prestamos/devolver_prestamo.html", {
        "prestamo": prestamo,
    })