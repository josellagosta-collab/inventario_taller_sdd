from django.shortcuts import render, get_object_or_404, redirect
from .models import Material, Categoria, MovimientoInventario
from .forms import MaterialForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
from documentos.models import Documento
from prestamos.models import Prestamo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from usuarios.decorators import pertenece_a_grupo
from django.http import HttpResponse
import openpyxl

@login_required
def lista_materiales(request):
    materiales = Material.objects.annotate(total_documentos=Count("documentos"))
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


@login_required
def detalle_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, "inventario/detalle_material.html", {
        "material": material
    })


@login_required
@pertenece_a_grupo("Administradores")
def crear_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST)

        if form.is_valid():
            material = form.save()
            MovimientoInventario.objects.create(
                material=material,
                tipo="alta",
                usuario=request.user if request.user.is_authenticated else None,
                descripcion="Alta de material desde la web"
            )
            return redirect("inventario:detalle_material", material_id=material.id)

    else:
        form = MaterialForm()

    return render(request, "inventario/crear_material.html", {
        "form": form
    })
    
@login_required
@pertenece_a_grupo("Administradores")
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
    
@login_required
@pertenece_a_grupo("Administradores")
def retirar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        material.estado = "retirado"
        material.save()
        MovimientoInventario.objects.create(
            material=material,
            tipo="retirada",
            usuario=request.user if request.user.is_authenticated else None,
            descripcion="Retirada lógica de material"
    )
        return redirect("inventario:lista_materiales")

    return render(request, "inventario/retirar_material.html", {
        "material": material
    })
    
@login_required
@pertenece_a_grupo("Administradores")
def lista_movimientos(request):
    movimientos = MovimientoInventario.objects.select_related(
        "material",
        "usuario"
    ).all()

    busqueda = request.GET.get("busqueda", "")
    tipo = request.GET.get("tipo", "")

    if busqueda:
        movimientos = movimientos.filter(
            Q(material__nombre__icontains=busqueda) |
            Q(material__codigo_inventario__icontains=busqueda) |
            Q(usuario__username__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    if tipo:
        movimientos = movimientos.filter(tipo=tipo)

    paginator = Paginator(movimientos, 10)
    numero_pagina = request.GET.get("page")
    pagina_movimientos = paginator.get_page(numero_pagina)

    return render(request, "inventario/lista_movimientos.html", {
        "movimientos": pagina_movimientos,
        "busqueda": busqueda,
        "tipo": tipo,
        "tipos_movimiento": MovimientoInventario.TIPOS_MOVIMIENTO,
    })
    
@login_required
def dashboard(request):
    hoy = timezone.now().date()

    total_materiales = Material.objects.count()
    materiales_disponibles = Material.objects.filter(estado="disponible").count()
    materiales_prestados = Material.objects.filter(estado="prestado").count()
    materiales_retirados = Material.objects.filter(estado="retirado").count()

    total_documentos = Documento.objects.count()

    prestamos_activos = Prestamo.objects.filter(estado="activo").count()

    prestamos_retrasados = Prestamo.objects.filter(
        estado="activo",
        fecha_prevista_devolucion__lt=hoy
    ).count()

    total_movimientos = MovimientoInventario.objects.count()

    return render(request, "inventario/dashboard.html", {
        "total_materiales": total_materiales,
        "materiales_disponibles": materiales_disponibles,
        "materiales_prestados": materiales_prestados,
        "materiales_retirados": materiales_retirados,
        "total_documentos": total_documentos,
        "prestamos_activos": prestamos_activos,
        "prestamos_retrasados": prestamos_retrasados,
        "total_movimientos": total_movimientos,
    })
    
@login_required
def exportar_materiales_excel(request):

    workbook = openpyxl.Workbook()

    hoja = workbook.active

    hoja.title = "Materiales"

    encabezados = [
        "Código",
        "Nombre",
        "Categoría",
        "Marca",
        "Modelo",
        "Cantidad",
        "Estado",
    ]

    for columna, texto in enumerate(encabezados, start=1):
        hoja.cell(row=1, column=columna, value=texto)

    materiales = Material.objects.all()

    fila = 2

    for material in materiales:

        hoja.cell(fila, 1, material.codigo_inventario)
        hoja.cell(fila, 2, material.nombre)

        hoja.cell(
            fila,
            3,
            material.categoria.nombre if material.categoria else ""
        )

        hoja.cell(fila, 4, material.marca)
        hoja.cell(fila, 5, material.modelo)
        hoja.cell(fila, 6, material.cantidad)
        hoja.cell(fila, 7, material.get_estado_display())

        fila += 1

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response[
        "Content-Disposition"
    ] = 'attachment; filename="inventario.xlsx"'

    workbook.save(response)

    return response