from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Incidencia
from inventario.models import Material, MovimientoInventario
from .forms import IncidenciaForm
from django.utils import timezone
from .forms import ResolverIncidenciaForm
from django.http import HttpResponse
import openpyxl


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


@login_required
def exportar_incidencias_excel(request):
    workbook = openpyxl.Workbook()
    hoja = workbook.active
    hoja.title = "Incidencias"

    encabezados = [
        "ID",
        "Título",
        "Material",
        "Código material",
        "Prioridad",
        "Estado",
        "Usuario",
        "Fecha creación",
        "Fecha cierre",
        "Solución",
    ]

    for columna, texto in enumerate(encabezados, start=1):
        hoja.cell(row=1, column=columna, value=texto)

    incidencias = Incidencia.objects.select_related(
        "material",
        "usuario"
    ).all()

    fila = 2

    for incidencia in incidencias:
        hoja.cell(fila, 1, incidencia.id)
        hoja.cell(fila, 2, incidencia.titulo)
        hoja.cell(fila, 3, incidencia.material.nombre)
        hoja.cell(fila, 4, incidencia.material.codigo_inventario)
        hoja.cell(fila, 5, incidencia.get_prioridad_display())
        hoja.cell(fila, 6, incidencia.get_estado_display())

        if incidencia.usuario:
            hoja.cell(fila, 7, incidencia.usuario.username)
        else:
            hoja.cell(fila, 7, "")

        hoja.cell(
            fila,
            8,
            incidencia.fecha_creacion.strftime("%d/%m/%Y %H:%M")
        )

        if incidencia.fecha_cierre:
            hoja.cell(
                fila,
                9,
                incidencia.fecha_cierre.strftime("%d/%m/%Y %H:%M")
            )
        else:
            hoja.cell(fila, 9, "")

        hoja.cell(fila, 10, incidencia.solucion or "")

        fila += 1

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="incidencias.xlsx"'

    workbook.save(response)

    return response