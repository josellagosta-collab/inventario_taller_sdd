from django.urls import path
from . import views

app_name = "prestamos"

urlpatterns = [
    path("prestamos/", views.lista_prestamos, name="lista_prestamos"),
    path("prestamos/nuevo/", views.crear_prestamo, name="crear_prestamo"),
    path("prestamos/<int:prestamo_id>/devolver/", views.devolver_prestamo, name="devolver_prestamo"),
    path("prestamos/<int:prestamo_id>/", views.detalle_prestamo, name="detalle_prestamo"),
    path("prestamos/exportar/excel/", views.exportar_prestamos_excel, name="exportar_prestamos_excel"),
    path("prestamos/exportar/pdf/", views.exportar_prestamos_pdf, name="exportar_prestamos_pdf"),
    path("reservas/nueva/", views.crear_reserva, name="crear_reserva"),
    path("reservas/", views.lista_reservas, name="lista_reservas"),
    path("reservas/<int:reserva_id>/cancelar/", views.cancelar_reserva, name="cancelar_reserva"),
    path("reservas/<int:reserva_id>/convertir/", views.convertir_reserva_en_prestamo, name="convertir_reserva_en_prestamo"),
    path("reservas/exportar/excel/", views.exportar_reservas_excel, name="exportar_reservas_excel"),
    path("reservas/exportar/pdf/", views.exportar_reservas_pdf, name="exportar_reservas_pdf"),
]