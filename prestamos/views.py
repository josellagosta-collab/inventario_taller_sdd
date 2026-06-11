from django.shortcuts import render, redirect
from .forms import PrestamoForm, LineaPrestamoForm


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