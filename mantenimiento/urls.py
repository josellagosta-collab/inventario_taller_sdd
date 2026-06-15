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
        "planes/",
        views.lista_planes_mantenimiento,
        name="lista_planes_mantenimiento",
    ),
    path(
        "materiales/<int:material_id>/mantenimientos/nuevo/",
        views.crear_mantenimiento_material,
        name="crear_mantenimiento_material",
    ),
    path(
        "materiales/<int:material_id>/planes/nuevo/",
        views.crear_plan_mantenimiento_material,
        name="crear_plan_mantenimiento_material",
    ),
]
