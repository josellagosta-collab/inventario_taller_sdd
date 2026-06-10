from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("materiales/", views.lista_materiales, name="lista_materiales"),
    path("materiales/<int:material_id>/", views.detalle_material, name="detalle_material"),
]