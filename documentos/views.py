from pathlib import Path

from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from auditoria.services import registrar_accion
from inventario.models import Material
from .forms import DocumentoForm
from .models import Documento
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from usuarios.decorators import pertenece_a_grupo

@login_required
@pertenece_a_grupo("Administradores")
def subir_documento(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == "POST":
        form = DocumentoForm(request.POST, request.FILES)

        if form.is_valid():
            documento = form.save(commit=False)
            documento.material = material

            if request.user.is_authenticated:
                documento.usuario = request.user

            documento.save()

            return redirect("inventario:detalle_material", material_id=material.id)

    else:
        form = DocumentoForm()

    return render(request, "documentos/subir_documento.html", {
        "form": form,
        "material": material,
    })
    
@login_required
@pertenece_a_grupo("Administradores")
def eliminar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    material = documento.material

    if request.method == "POST":
        documento.archivo.delete(save=False)
        documento.delete()
        return redirect("inventario:detalle_material", material_id=material.id)

    return render(request, "documentos/eliminar_documento.html", {
        "documento": documento,
        "material": material,
    })
    
@login_required
def lista_documentos(request):
    documentos = Documento.objects.select_related("material", "usuario").all()

    busqueda = request.GET.get("busqueda", "")
    tipo_documento = request.GET.get("tipo_documento", "")

    if busqueda:
        documentos = documentos.filter(
            Q(nombre__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(material__nombre__icontains=busqueda) |
            Q(material__codigo_inventario__icontains=busqueda)
        )

    if tipo_documento:
        documentos = documentos.filter(tipo_documento=tipo_documento)

    paginator = Paginator(documentos, 10)
    numero_pagina = request.GET.get("page")
    pagina_documentos = paginator.get_page(numero_pagina)

    return render(request, "documentos/lista_documentos.html", {
        "documentos": pagina_documentos,
        "busqueda": busqueda,
        "tipo_documento": tipo_documento,
        "tipos_documento": Documento.TIPOS_DOCUMENTO,
    })


@login_required
def descargar_documento(request, documento_id):
    documento = get_object_or_404(
        Documento.objects.select_related("material"),
        id=documento_id,
    )

    if not documento.archivo:
        raise Http404("El documento no tiene archivo asociado.")

    ruta_archivo = Path(documento.archivo.path)

    if not ruta_archivo.exists():
        raise Http404("El archivo no existe.")

    registrar_accion(
        request,
        "acceder",
        f"Descarga de documento: {documento.nombre}",
        documento,
    )

    return FileResponse(
        documento.archivo.open("rb"),
        as_attachment=True,
        filename=ruta_archivo.name,
    )
