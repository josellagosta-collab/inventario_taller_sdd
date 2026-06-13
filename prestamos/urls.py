from django.urls import path
from . import views

app_name = "prestamos"

urlpatterns = [
    path("prestamos/", views.lista_prestamos, name="lista_prestamos"),
    path("prestamos/nuevo/", views.crear_prestamo, name="crear_prestamo"),
    path("prestamos/<int:prestamo_id>/devolver/", views.devolver_prestamo, name="devolver_prestamo"),
    path("prestamos/<int:prestamo_id>/", views.detalle_prestamo, name="detalle_prestamo"),
    path("prestamos/exportar/excel/", views.exportar_prestamos_excel, name="exportar_prestamos_excel"),
]