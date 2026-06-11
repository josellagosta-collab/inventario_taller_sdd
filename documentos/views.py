from django.shortcuts import render, get_object_or_404, redirect
from inventario.models import Material
from .forms import DocumentoForm
from .models import Documento

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
    
def lista_documentos(request):
    documentos = Documento.objects.select_related("material", "usuario").all()

    return render(request, "documentos/lista_documentos.html", {
        "documentos": documentos,
    })
