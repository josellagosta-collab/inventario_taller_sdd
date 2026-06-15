from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, F, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from incidencias.models import Incidencia
from inventario.models import Categoria, Material
from prestamos.models import Prestamo
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


@login_required
@pertenece_a_grupo("Administradores")
def informe_prestamos(request):
    prestamos = Prestamo.objects.select_related(
        "usuario_receptor",
        "profesor_responsable",
    ).prefetch_related(
        "lineas__material",
    ).all()

    estado = request.GET.get("estado", "")
    usuario_receptor = request.GET.get("usuario_receptor", "")
    profesor_responsable = request.GET.get("profesor_responsable", "")
    retrasados = request.GET.get("retrasados", "")
    busqueda = request.GET.get("busqueda", "")

    if estado:
        prestamos = prestamos.filter(estado=estado)

    if usuario_receptor:
        prestamos = prestamos.filter(usuario_receptor_id=usuario_receptor)

    if profesor_responsable:
        prestamos = prestamos.filter(profesor_responsable_id=profesor_responsable)

    if busqueda:
        prestamos = prestamos.filter(
            Q(usuario_receptor__username__icontains=busqueda) |
            Q(profesor_responsable__username__icontains=busqueda) |
            Q(lineas__material__nombre__icontains=busqueda) |
            Q(lineas__material__codigo_inventario__icontains=busqueda)
        )

    if retrasados == "1":
        prestamos = prestamos.filter(
            estado="activo",
            fecha_prevista_devolucion__lt=timezone.now().date(),
        )

    prestamos = prestamos.distinct()
    hoy = timezone.now().date()
    total_prestamos = prestamos.count()
    total_activos = prestamos.filter(estado="activo").count()
    total_devueltos = prestamos.filter(estado="devuelto").count()
    total_retrasados = prestamos.filter(
        estado="activo",
        fecha_prevista_devolucion__lt=hoy,
    ).count()
    total_materiales_prestados = sum(
        linea.cantidad
        for prestamo in prestamos
        for linea in prestamo.lineas.all()
    )

    por_estado = prestamos.values("estado").annotate(
        total=Count("id")
    ).order_by("estado")
    por_profesor = prestamos.values(
        "profesor_responsable__username"
    ).annotate(
        total=Count("id")
    ).order_by("profesor_responsable__username")

    return render(request, "informes/informe_prestamos.html", {
        "prestamos": prestamos,
        "usuarios": User.objects.all(),
        "estados": Prestamo.ESTADOS,
        "estado": estado,
        "usuario_receptor": usuario_receptor,
        "profesor_responsable": profesor_responsable,
        "retrasados": retrasados,
        "busqueda": busqueda,
        "total_prestamos": total_prestamos,
        "total_activos": total_activos,
        "total_devueltos": total_devueltos,
        "total_retrasados": total_retrasados,
        "total_materiales_prestados": total_materiales_prestados,
        "por_estado": por_estado,
        "por_profesor": por_profesor,
    })


@login_required
@pertenece_a_grupo("Administradores")
def informe_incidencias(request):
    incidencias = Incidencia.objects.select_related(
        "material",
        "usuario",
    ).all()

    busqueda = request.GET.get("busqueda", "")
    prioridad = request.GET.get("prioridad", "")
    estado = request.GET.get("estado", "")
    abiertas = request.GET.get("abiertas", "")

    if busqueda:
        incidencias = incidencias.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(material__nombre__icontains=busqueda) |
            Q(material__codigo_inventario__icontains=busqueda) |
            Q(usuario__username__icontains=busqueda)
        )

    if prioridad:
        incidencias = incidencias.filter(prioridad=prioridad)

    if estado:
        incidencias = incidencias.filter(estado=estado)

    if abiertas == "1":
        incidencias = incidencias.exclude(estado="cerrada")

    incidencias = incidencias.distinct()
    total_incidencias = incidencias.count()
    total_abiertas = incidencias.exclude(estado="cerrada").count()
    total_cerradas = incidencias.filter(estado="cerrada").count()
    total_criticas = incidencias.filter(
        prioridad="critica",
    ).exclude(
        estado="cerrada",
    ).count()
    total_reparacion = incidencias.filter(estado="en_reparacion").count()

    por_estado = incidencias.values("estado").annotate(
        total=Count("id")
    ).order_by("estado")
    por_prioridad = incidencias.values("prioridad").annotate(
        total=Count("id")
    ).order_by("prioridad")
    por_material = incidencias.values(
        "material__nombre",
        "material__codigo_inventario",
    ).annotate(
        total=Count("id")
    ).order_by("-total", "material__nombre")[:10]

    return render(request, "informes/informe_incidencias.html", {
        "incidencias": incidencias,
        "prioridades": Incidencia.PRIORIDADES,
        "estados": Incidencia.ESTADOS,
        "busqueda": busqueda,
        "prioridad": prioridad,
        "estado": estado,
        "abiertas": abiertas,
        "total_incidencias": total_incidencias,
        "total_abiertas": total_abiertas,
        "total_cerradas": total_cerradas,
        "total_criticas": total_criticas,
        "total_reparacion": total_reparacion,
        "por_estado": por_estado,
        "por_prioridad": por_prioridad,
        "por_material": por_material,
    })
