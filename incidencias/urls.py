from django.urls import path
from . import views

app_name = "incidencias"

urlpatterns = [
    path(
        "materiales/<int:material_id>/incidencias/nueva/",
        views.crear_incidencia,
        name="crear_incidencia"
    ),
    
    path(
    "incidencias/",
    views.lista_incidencias,
    name="lista_incidencias"
    ),  
    path(
    "incidencias/<int:incidencia_id>/",
    views.detalle_incidencia,
    name="detalle_incidencia"
    ),
    
    path(
    "incidencias/<int:incidencia_id>/resolver/",
    views.resolver_incidencia,
    name="resolver_incidencia"
    ),
    path(
    "incidencias/exportar/excel/",
    views.exportar_incidencias_excel,
    name="exportar_incidencias_excel"
    ),
    
]