from django.urls import path
from . import views

app_name = "documentos"

urlpatterns = [
    path(
        "materiales/<int:material_id>/documentos/subir/",
        views.subir_documento,
        name="subir_documento"
    ),
]