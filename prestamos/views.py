from .forms import PrestamoForm, LineaPrestamoForm
from .models import Prestamo
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from inventario.models import MovimientoInventario
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import openpyxl

@login_required
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

            MovimientoInventario.objects.create(
                material=material,
                tipo="prestamo",
                usuario=request.user if request.user.is_authenticated else None,
                descripcion=f"Préstamo registrado. Préstamo ID: {prestamo.id}"
        )
          

            return redirect("prestamos:lista_prestamos")

    else:
        prestamo_form = PrestamoForm()
        linea_form = LineaPrestamoForm()

    return render(request, "prestamos/crear_prestamo.html", {
        "prestamo_form": prestamo_form,
        "linea_form": linea_form,
    })
    
@login_required
def lista_prestamos(request):
    prestamos = Prestamo.objects.select_related(
        "usuario_receptor",
        "profesor_responsable"
    ).prefetch_related("lineas__material")

    usuarios = User.objects.all()

    estado = request.GET.get("estado", "")
    usuario_receptor = request.GET.get("usuario_receptor", "")
    profesor_responsable = request.GET.get("profesor_responsable", "")

    if estado:
        prestamos = prestamos.filter(estado=estado)

    if usuario_receptor:
        prestamos = prestamos.filter(usuario_receptor_id=usuario_receptor)

    if profesor_responsable:
        prestamos = prestamos.filter(profesor_responsable_id=profesor_responsable)

    hoy = timezone.now().date()

    total_prestamos = Prestamo.objects.count()

    total_activos = Prestamo.objects.filter(
        estado="activo"
    ).count()

    total_devueltos = Prestamo.objects.filter(
        estado="devuelto"
    ).count()

    total_retrasados = Prestamo.objects.filter(
        estado="activo",
        fecha_prevista_devolucion__lt=hoy
    ).count()

    paginator = Paginator(prestamos, 10)
    numero_pagina = request.GET.get("page")
    pagina_prestamos = paginator.get_page(numero_pagina)

    return render(request, "prestamos/lista_prestamos.html", {
        "prestamos": pagina_prestamos,
        "usuarios": usuarios,
        "estado": estado,
        "usuario_receptor": usuario_receptor,
        "profesor_responsable": profesor_responsable,
        "estados": Prestamo.ESTADOS,
        "total_prestamos": total_prestamos,
        "total_activos": total_activos,
        "total_devueltos": total_devueltos,
        "total_retrasados": total_retrasados,
    })
    
@login_required
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
            MovimientoInventario.objects.create(
                material=material,
                tipo="devolucion",
                usuario=request.user if request.user.is_authenticated else None,
                descripcion=f"Devolución registrada. Préstamo ID: {prestamo.id}"
            )

        return redirect("prestamos:lista_prestamos")
    
        hoy = timezone.now().date()

    total_prestamos = Prestamo.objects.count()

    total_activos = Prestamo.objects.filter(
        estado="activo"
    ).count()

    total_devueltos = Prestamo.objects.filter(
        estado="devuelto"
    ).count()

    total_retrasados = Prestamo.objects.filter(
        estado="activo",
        fecha_prevista_devolucion__lt=hoy
    ).count()

    return render(request, "prestamos/devolver_prestamo.html", {
        "prestamo": prestamo,
        "total_prestamos": total_prestamos,
        "total_activos": total_activos,
        "total_devueltos": total_devueltos,
        "total_retrasados": total_retrasados,
    })
    
@login_required
def detalle_prestamo(request, prestamo_id):
    prestamo = get_object_or_404(
        Prestamo.objects.select_related(
            "usuario_receptor",
            "profesor_responsable"
        ).prefetch_related("lineas__material"),
        id=prestamo_id
    )

    return render(request, "prestamos/detalle_prestamo.html", {
        "prestamo": prestamo,
    })
    
@login_required
def exportar_prestamos_excel(request):
    workbook = openpyxl.Workbook()
    hoja = workbook.active
    hoja.title = "Prestamos"

    encabezados = [
        "ID",
        "Usuario receptor",
        "Profesor responsable",
        "Materiales",
        "Fecha préstamo",
        "Fecha prevista devolución",
        "Fecha devolución real",
        "Estado",
    ]

    for columna, texto in enumerate(encabezados, start=1):
        hoja.cell(row=1, column=columna, value=texto)

    prestamos = Prestamo.objects.select_related(
        "usuario_receptor",
        "profesor_responsable"
    ).prefetch_related("lineas__material")

    fila = 2

    for prestamo in prestamos:
        materiales = ", ".join(
            [
                f"{linea.material.nombre} x {linea.cantidad}"
                for linea in prestamo.lineas.all()
            ]
        )

        hoja.cell(fila, 1, prestamo.id)
        hoja.cell(fila, 2, prestamo.usuario_receptor.username)
        hoja.cell(fila, 3, prestamo.profesor_responsable.username)
        hoja.cell(fila, 4, materiales)
        hoja.cell(fila, 5, prestamo.fecha_prestamo)
        hoja.cell(fila, 6, prestamo.fecha_prevista_devolucion)
        hoja.cell(fila, 7, prestamo.fecha_devolucion_real)
        hoja.cell(fila, 8, prestamo.get_estado_display())

        fila += 1

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response["Content-Disposition"] = 'attachment; filename="prestamos.xlsx"'

    workbook.save(response)

    return response