from django.urls import path
from . import views

app_name = "incidencias"

urlpatterns = [
    path(
        "materiales/<int:material_id>/incidencias/nueva/",
        views.crear_incidencia,
        name="crear_incidencia"
    ),
]