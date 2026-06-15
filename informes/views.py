from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q, Sum
from django.shortcuts import render

from inventario.models import Categoria, Material
from usuarios.decorators import pertenece_a_grupo


@login_required
@pertenece_a_grupo("Administradores")
def panel_informes(request):
    return render(request, "informes/panel_informes.html")


@login_required
@pertenece_a_grupo("Administradores")
def informe_inventario(request):
    materiales = Material.objects.select_related(
        "categoria",
        "subcategoria",
        "proveedor",
        "ubicacion",
    ).all()

    busqueda = request.GET.get("busqueda", "")
    categoria_id = request.GET.get("categoria", "")
    estado = request.GET.get("estado", "")
    stock_bajo = request.GET.get("stock_bajo", "")

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

    if stock_bajo == "1":
        materiales = materiales.filter(cantidad__lte=F("stock_minimo"))

    materiales = materiales.distinct()
    resumen = materiales.aggregate(
        total_materiales=Count("id"),
        total_unidades=Sum("cantidad"),
    )
    valor_total = sum(
        (material.precio_compra or 0) * material.cantidad
        for material in materiales
    )
    total_materiales = resumen["total_materiales"] or 0
    total_unidades = resumen["total_unidades"] or 0
    total_stock_bajo = materiales.filter(
        cantidad__lte=F("stock_minimo")
    ).count()
    total_sin_ubicacion = materiales.filter(ubicacion__isnull=True).count()

    por_estado = materiales.values("estado").annotate(
        total=Count("id")
    ).order_by("estado")
    por_categoria = materiales.values(
        "categoria__nombre"
    ).annotate(
        total=Count("id"),
        unidades=Sum("cantidad"),
    ).order_by("categoria__nombre")

    return render(request, "informes/informe_inventario.html", {
        "materiales": materiales,
        "categorias": Categoria.objects.all(),
        "estados": Material.ESTADOS,
        "busqueda": busqueda,
        "categoria_id": categoria_id,
        "estado": estado,
        "stock_bajo": stock_bajo,
        "total_materiales": total_materiales,
        "total_unidades": total_unidades,
        "total_stock_bajo": total_stock_bajo,
        "total_sin_ubicacion": total_sin_ubicacion,
        "valor_total": valor_total,
        "por_estado": por_estado,
        "por_categoria": por_categoria,
    })
