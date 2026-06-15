from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from auditoria.services import registrar_accion
from inventario.models import Material, MovimientoInventario
from usuarios.decorators import pertenece_a_grupo

from .forms import MantenimientoForm, PlanMantenimientoForm
from .models import Mantenimiento, PlanMantenimiento


@login_required
def lista_mantenimientos(request):
    mantenimientos = Mantenimiento.objects.select_related(
        "material",
        "tecnico",
    ).all()

    busqueda = request.GET.get("busqueda", "")
    tipo = request.GET.get("tipo", "")
    resultado = request.GET.get("resultado", "")
    fecha_desde = request.GET.get("fecha_desde", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")

    if busqueda:
        mantenimientos = mantenimientos.filter(
            Q(material__nombre__icontains=busqueda) |
            Q(material__codigo_inventario__icontains=busqueda) |
            Q(tecnico__username__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(observaciones__icontains=busqueda)
        )

    if tipo:
        mantenimientos = mantenimientos.filter(tipo=tipo)

    if resultado:
        mantenimientos = mantenimientos.filter(resultado=resultado)

    if fecha_desde:
        mantenimientos = mantenimientos.filter(fecha__gte=fecha_desde)

    if fecha_hasta:
        mantenimientos = mantenimientos.filter(fecha__lte=fecha_hasta)

    paginator = Paginator(mantenimientos, 10)
    numero_pagina = request.GET.get("page")
    pagina_mantenimientos = paginator.get_page(numero_pagina)

    return render(request, "mantenimiento/lista_mantenimientos.html", {
        "mantenimientos": pagina_mantenimientos,
        "busqueda": busqueda,
        "tipo": tipo,
        "resultado": resultado,
        "fecha_desde": fecha_desde,
        "fecha_hasta": fecha_hasta,
        "tipos": Mantenimiento.TIPOS,
        "resultados": Mantenimiento.RESULTADOS,
    })


@login_required
def lista_planes_mantenimiento(request):
    hoy = timezone.now().date()
    fecha_limite_alerta = hoy + timedelta(
        days=PlanMantenimiento.DIAS_ALERTA_REVISION
    )
    planes = PlanMantenimiento.objects.select_related(
        "material",
        "responsable",
    ).all()

    busqueda = request.GET.get("busqueda", "")
    tipo = request.GET.get("tipo", "")
    activo = request.GET.get("activo", "")
    fecha_hasta = request.GET.get("fecha_hasta", "")
    alerta = request.GET.get("alerta", "")

    if busqueda:
        planes = planes.filter(
            Q(nombre__icontains=busqueda) |
            Q(material__nombre__icontains=busqueda) |
            Q(material__codigo_inventario__icontains=busqueda) |
            Q(responsable__username__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(observaciones__icontains=busqueda)
        )

    if tipo:
        planes = planes.filter(tipo=tipo)

    if activo == "1":
        planes = planes.filter(activo=True)
    elif activo == "0":
        planes = planes.filter(activo=False)

    if fecha_hasta:
        planes = planes.filter(proxima_revision__lte=fecha_hasta)

    total_vencidos = planes.filter(
        activo=True,
        proxima_revision__lt=hoy,
    ).count()
    total_proximos = planes.filter(
        activo=True,
        proxima_revision__gte=hoy,
        proxima_revision__lte=fecha_limite_alerta,
    ).count()

    if alerta == "vencidos":
        planes = planes.filter(
            activo=True,
            proxima_revision__lt=hoy,
        )
    elif alerta == "proximos":
        planes = planes.filter(
            activo=True,
            proxima_revision__gte=hoy,
            proxima_revision__lte=fecha_limite_alerta,
        )
    elif alerta == "pendientes":
        planes = planes.filter(
            activo=True,
            proxima_revision__lte=fecha_limite_alerta,
        )

    paginator = Paginator(planes, 10)
    numero_pagina = request.GET.get("page")
    pagina_planes = paginator.get_page(numero_pagina)

    return render(request, "mantenimiento/lista_planes_mantenimiento.html", {
        "planes": pagina_planes,
        "busqueda": busqueda,
        "tipo": tipo,
        "activo": activo,
        "fecha_hasta": fecha_hasta,
        "alerta": alerta,
        "total_vencidos": total_vencidos,
        "total_proximos": total_proximos,
        "tipos": Mantenimiento.TIPOS,
    })


@login_required
@pertenece_a_grupo("Administradores")
def crear_mantenimiento_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = MantenimientoForm(request.POST)

        if form.is_valid():
            mantenimiento = form.save(commit=False)
            mantenimiento.material = material

            if request.user.is_authenticated:
                mantenimiento.tecnico = request.user

            mantenimiento.save()

            descripcion = (
                f"Mantenimiento registrado. "
                f"Tipo: {mantenimiento.get_tipo_display()}. "
                f"Resultado: {mantenimiento.get_resultado_display()}."
            )
            MovimientoInventario.objects.create(
                material=material,
                tipo="ajuste",
                usuario=request.user if request.user.is_authenticated else None,
                descripcion=descripcion,
            )
            registrar_accion(
                request,
                "crear",
                descripcion,
                mantenimiento,
            )
            return redirect("inventario:detalle_material", material_id=material.id)
    else:
        form = MantenimientoForm()

    return render(request, "mantenimiento/form_mantenimiento.html", {
        "form": form,
        "material": material,
    })


@login_required
@pertenece_a_grupo("Administradores")
def crear_plan_mantenimiento_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = PlanMantenimientoForm(request.POST)

        if form.is_valid():
            plan = form.save(commit=False)
            plan.material = material

            if request.user.is_authenticated:
                plan.responsable = request.user

            plan.save()

            descripcion = (
                f"Plan de mantenimiento creado. "
                f"Nombre: {plan.nombre}. "
                f"Tipo: {plan.get_tipo_display()}. "
                f"Próxima revisión: {plan.proxima_revision}."
            )
            registrar_accion(
                request,
                "crear",
                descripcion,
                plan,
            )
            return redirect("inventario:detalle_material", material_id=material.id)
    else:
        form = PlanMantenimientoForm()

    return render(request, "mantenimiento/form_plan_mantenimiento.html", {
        "form": form,
        "material": material,
    })
