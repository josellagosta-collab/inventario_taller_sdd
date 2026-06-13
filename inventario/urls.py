from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("materiales/", views.lista_materiales, name="lista_materiales"),
    path("materiales/nuevo/", views.crear_material, name="crear_material"),
    path("materiales/<int:material_id>/", views.detalle_material, name="detalle_material"),
    path("materiales/<int:material_id>/editar/", views.editar_material, name="editar_material"),
    path("materiales/<int:material_id>/retirar/", views.retirar_material, name="retirar_material"),
    path("movimientos/", views.lista_movimientos, name="lista_movimientos"),
    path("", views.dashboard, name="dashboard"),
    path("materiales/exportar/excel/", views.exportar_materiales_excel, name="exportar_materiales_excel"),
    path("materiales/exportar/pdf/", views.exportar_materiales_pdf, name="exportar_materiales_pdf"),
    path("movimientos/exportar/excel/", views.exportar_movimientos_excel, name="exportar_movimientos_excel"),
    path("movimientos/exportar/pdf/", views.exportar_movimientos_pdf, name="exportar_movimientos_pdf"),
]