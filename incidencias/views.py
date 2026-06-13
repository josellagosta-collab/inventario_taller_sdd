from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Incidencia
from inventario.models import Material, MovimientoInventario
from .forms import IncidenciaForm
from django.utils import timezone
from .forms import ResolverIncidenciaForm


@login_required
def crear_incidencia(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = IncidenciaForm(request.POST)

        if form.is_valid():
            incidencia = form.save(commit=False)
            incidencia.material = material

            if request.user.is_authenticated:
                incidencia.usuario = request.user

            incidencia.save()

            material.estado = "averiado"
            material.save()

            MovimientoInventario.objects.create(
                material=material,
                tipo="edicion",
                usuario=request.user if request.user.is_authenticated else None,
                descripcion=f"Incidencia creada: {incidencia.titulo}"
            )

            return redirect("inventario:detalle_material", material_id=material.id)

    else:
        form = IncidenciaForm()

    return render(request, "incidencias/crear_incidencia.html", {
        "form": form,
        "material": material,
    })
    
@login_required
def lista_incidencias(request):
    incidencias = Incidencia.objects.select_related(
        "material",
        "usuario"
    ).all()

    return render(request, "incidencias/lista_incidencias.html", {
        "incidencias": incidencias,
    })
    
@login_required
def detalle_incidencia(request, incidencia_id):
    incidencia = get_object_or_404(
        Incidencia.objects.select_related(
            "material",
            "usuario"
        ).prefetch_related(
            "comentarios__usuario"
        ),
        id=incidencia_id
    )

    return render(request, "incidencias/detalle_incidencia.html", {
        "incidencia": incidencia,
    })
    
@login_required
def resolver_incidencia(request, incidencia_id):

    incidencia = get_object_or_404(
        Incidencia,
        id=incidencia_id
    )

    if request.method == "POST":

        form = ResolverIncidenciaForm(request.POST)

        if form.is_valid():

            incidencia.solucion = form.cleaned_data["solucion"]

            incidencia.estado = "cerrada"

            incidencia.fecha_cierre = timezone.now()

            incidencia.save()

            material = incidencia.material

            material.estado = "disponible"

            material.save()

            MovimientoInventario.objects.create(
                material=material,
                tipo="edicion",
                usuario=request.user,
                descripcion=f"Incidencia resuelta: {incidencia.titulo}"
            )

            return redirect(
                "incidencias:detalle_incidencia",
                incidencia.id
            )

    else:

        form = ResolverIncidenciaForm()

    return render(
        request,
        "incidencias/resolver_incidencia.html",
        {
            "incidencia": incidencia,
            "form": form,
        }
    )