from django.urls import path
from . import views

app_name = "documentos"

urlpatterns = [
    path(
        "documentos/",
        views.lista_documentos,
        name="lista_documentos"
    ),
    path(
        "materiales/<int:material_id>/documentos/subir/",
        views.subir_documento,
        name="subir_documento"
    ),
    path(
        "documentos/<int:documento_id>/descargar/",
        views.descargar_documento,
        name="descargar_documento"
    ),
    path(
        "documentos/<int:documento_id>/eliminar/",
        views.eliminar_documento,
        name="eliminar_documento"
    ),
]
