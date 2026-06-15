from django.urls import path

from . import views

app_name = "mantenimiento"

urlpatterns = [
    path(
        "mantenimientos/",
        views.lista_mantenimientos,
        name="lista_mantenimientos",
    ),
    path(
        "materiales/<int:material_id>/mantenimientos/nuevo/",
        views.crear_mantenimiento_material,
        name="crear_mantenimiento_material",
    ),
]
